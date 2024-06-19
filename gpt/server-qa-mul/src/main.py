#!/usr/bin/env python
# encoding: utf-8

import os
import tornado.ioloop
import tornado.web
import logging
import env
import glo
import multiprocessing
from log import init_basic_logger
from multiprocessing import pool

init_basic_logger()

from openai_api import GPT
from handler import HealthHandler, QaHandler, SummaryAndQuestionsHandler

glo.init()

logger = logging.getLogger(__name__)

routes = [
    ("/health", HealthHandler),
    ("/qa", QaHandler),
    ("/summary_questions", SummaryAndQuestionsHandler),
]


def init_process_pool():
    logger.info("init_process_pool")
    ctx = multiprocessing.get_context("spawn")
    client_ids = ctx.Value('i', 0)
    process_pool = pool.Pool(processes=len(env.OPENAI_KEYS),
                             initializer=init_sub_process,
                             initargs=(client_ids,))
    glo.set_value('process_pool', process_pool)


def init_sub_process(client_ids):
    """子进程启动的时候执行的初始化函数"""
    with client_ids.get_lock():
        api_key = env.OPENAI_KEYS[client_ids.value]
        GPT.init_key(api_key)
        logger.info(f"init_sub_process pid:{os.getpid()} {api_key}")
        client_ids.value += 1


def start():
    master_pid = os.getpid()
    logger.info(f"master_pid:{master_pid}")
    init_process_pool()
    application = tornado.web.Application(routes)
    application.listen(env.PORT)
    logger.info("Start!")
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    start()
