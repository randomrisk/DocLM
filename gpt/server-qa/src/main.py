#!/usr/bin/env python
# encoding: utf-8

import tornado.ioloop
import tornado.web
import logging
import env
from log import init_basic_logger

init_basic_logger()

from handler import HealthHandler, SummaryAndQuestionsHandler

logger = logging.getLogger(__name__)

routes = [
    ("/health", HealthHandler),
    ("/summary_questions", SummaryAndQuestionsHandler),
]


def start():
    application = tornado.web.Application(routes)
    application.listen(env.PORT)
    logger.info("Start!!")
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    start()
