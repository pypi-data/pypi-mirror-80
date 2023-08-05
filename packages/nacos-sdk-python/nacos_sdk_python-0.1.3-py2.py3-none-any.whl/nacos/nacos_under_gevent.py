import datetime
import logging
from threading import Thread
try:
    # python3.x
    from queue import Queue
except ImportError:
    # python2.x
    from Queue import Queue

from nacos import NacosClient, NacosException
from nacos.client import process_common_config_params, WatcherWrap, DEFAULTS
from nacos.commons import synchronized_with_attr
from nacos.params import group_key, parse_key
from apscheduler.schedulers.background import BackgroundScheduler
logger = logging.getLogger(__name__)


class NacosClient4Gevent(NacosClient):
    def __init__(self, server_addresses, endpoint=None, namespace=None, ak=None, sk=None, username=None, password=None):
        NacosClient.__init__(self, server_addresses, endpoint, namespace, ak, sk, username, password)
        # self.callback_thread_num = DEFAULTS["CALLBACK_THREAD_NUM"]
        self.scheduler = None
        self.silent_period_mapping = None

    @synchronized_with_attr("pulling_lock")
    def add_config_watcher(self, data_id, group, cb, content=None, silent_period=0):
        self.add_config_watchers(data_id, group, [cb], content, silent_period)

    @synchronized_with_attr("pulling_lock")
    def add_config_watchers(self, data_id, group, cb_list, content=None, silent_period=0):
        if not cb_list:
            raise NacosException("A callback function is needed.")
        data_id, group = process_common_config_params(data_id, group)
        logger.info("[add-watcher] data_id:%s, group:%s, namespace:%s" % (data_id, group, self.namespace))
        cache_key = group_key(data_id, group, self.namespace)
        wl = self.watcher_mapping.get(cache_key)
        if not wl:
            wl = list()
            self.watcher_mapping[cache_key] = wl
        if not content:
            content = self.get_config(data_id, group)
        last_md5 = NacosClient.get_md5(content)
        for cb in cb_list:
            wl.append(WatcherWrap(cache_key, cb, last_md5))
            logger.info("[add-watcher] watcher has been added for key:%s, new callback is:%s, callback number is:%s" % (
                cache_key, cb.__name__, len(wl)))

        if self.puller_mapping is None:
            logger.debug("[add-watcher] pulling should be initialized")
            self._init_pulling()
        self.silent_period_mapping[cache_key] = silent_period
        if cache_key in self.puller_mapping:
            logger.debug("[add-watcher] key:%s is already in pulling" % cache_key)
            return

        for key, puller_info in self.puller_mapping.items():
            if len(puller_info[1]) < self.pulling_config_size:
                logger.debug("[add-watcher] puller:%s is available, add key:%s" % (puller_info[0], cache_key))
                puller_info[1].append(cache_key)
                self.puller_mapping[cache_key] = puller_info
                break
        else:
            logger.debug("[add-watcher] no puller available, new one and add key:%s" % cache_key)
            key_list = []  # self.process_mgr.list()
            key_list.append(cache_key)


            puller = Thread(target=self._do_pulling, args=(key_list, self.notify_queue))
            puller.setDaemon(True)

            puller.start()
            self.puller_mapping[cache_key] = (puller, key_list)

    @synchronized_with_attr("pulling_lock")
    def _init_pulling(self):
        if self.puller_mapping is not None:
            logger.info("[init-pulling] puller is already initialized")
            return

        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.puller_mapping = dict()
        self.silent_period_mapping = dict()
        self.notify_queue = Queue()
        # self.callback_tread_pool = pool.ThreadPool(self.callback_thread_num)
        # self.process_mgr = Manager() TODO
        t = Thread(target=self._process_polling_result)
        t.setDaemon(True)
        t.start()
        logger.info("[init-pulling] init completed")

    def _process_polling_result(self):
        while True:
            cache_key, content, md5 = self.notify_queue.get()
            logger.debug("[process-polling-result] receive an event:%s" % cache_key)
            wl = self.watcher_mapping.get(cache_key)
            if not wl:
                logger.warning("[process-polling-result] no watcher on %s, ignored" % cache_key)
                continue

            data_id, group, namespace = parse_key(cache_key)
            plain_content = content

            params = {
                "data_id": data_id,
                "group": group,
                "namespace": namespace,
                "raw_content": content,
                "content": plain_content,
            }
            for watcher in wl:
                if not watcher.last_md5 == md5:
                    logger.debug(
                        "[process-polling-result] md5 changed since last call, calling %s with changed params: %s"
                        % (watcher.callback.__name__, params))
                    try:
                        job = self.scheduler.get_job(cache_key)
                        silent_period = self.silent_period_mapping[cache_key]
                        if job:
                            self.scheduler.modify_job(cache_key, func=watcher.callback, args=(params,),
                                                 next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=silent_period))
                        else:
                            self.scheduler.add_job(func=watcher.callback, args=(params,),
                                                    next_run_time=datetime.datetime.now() + datetime.timedelta(
                                                        seconds=silent_period), id=cache_key)
                        # self.callback_tread_pool.apply(watcher.callback, (params,))
                    except Exception as e:
                        logger.exception("[process-polling-result] exception %s occur while calling %s " % (
                            str(e), watcher.callback.__name__))
                    watcher.last_md5 = md5
