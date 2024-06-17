#!/usr/bin/env python
# encoding: utf-8

import json
import logging
import random

import env
import tornado.web
from openai_api import get_questions, get_summary
from utils import resp_error, resp_success
from concurrent.futures.thread import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
import concurrent.futures

logger = logging.getLogger(__name__)


class HealthHandler(tornado.web.RequestHandler):
    def get(self):
        logger.info('qwert')
        self.write("OK")


class BaseHandler(tornado.web.RequestHandler):
    def write(self, chunk):
        if isinstance(chunk, dict):
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            chunk = json.dumps(chunk, ensure_ascii=False)
        return super().write(chunk)


class SummaryAndQuestionsHandler(BaseHandler):
    """
        生成总结并提问
    """
    executor = ThreadPoolExecutor(max_workers=10)

    @run_on_executor
    def post(self):
        if self.request.body:
            params = json.loads(self.request.body)
        else:
            params = {}
        context = params.get('context')
        auth_code = params.get('auth_code')
        model = params.get('model')
        if auth_code != env.AUTH_CODE or model not in ['gpt-3.5-turbo', 'text-curie-001']:
            self.write(resp_error('参数错误'))
            logger.exception(f"SummaryAndQuestionsHandler 参数错误 auth_code:{auth_code} ip:{self.request.remote_ip}")
            return
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                all_task = [
                    executor.submit(get_summary, random.choice(env.OPENAI_KEYS), context, model),
                    executor.submit(get_questions, random.choice(env.OPENAI_KEYS), context, model)
                ]
                res = {}
                for future in concurrent.futures.as_completed(all_task):  # 并发执行
                    key, data = future.result()
                    res[key] = data
                logger.info(f"{res}")
                self.write(resp_success(res))
        except Exception as e:
            logger.exception(f"SummaryAndQuestionsHandler error {e}")
            self.write(resp_error())
