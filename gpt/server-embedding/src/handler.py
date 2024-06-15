#!/usr/bin/env python
# encoding: utf-8

import json
import logging
import env
import glo
import tornado.web
import multiprocessing
from typing import List
from utils import resp_success, resp_error
from concurrent.futures.thread import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
from openai_api import GPT

logger = logging.getLogger(__name__)


class HealthHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("OK")


class BaseHandler(tornado.web.RequestHandler):
    def write(self, chunk):
        if isinstance(chunk, dict):
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            chunk = json.dumps(chunk, ensure_ascii=False)
        return super().write(chunk)


def async_process(text: List[str]):
    process_pool = glo.get_value('process_pool')
    t = process_pool.apply_async(GPT.get_embedding, (text,))
    try:
        result = t.get(timeout=env.PROCESS_TIMEOUT)
        if result:
            return True, result
        return False, None
    except multiprocessing.context.TimeoutError:
        logger.error(f"async task process timeout after {env.PROCESS_TIMEOUT}s")
        return False, None
    except Exception as e:
        logger.exception(f"async task process error {e}")
        return False, None


class EmbeddingHandler(BaseHandler):
    """
        对话
    """
    executor = ThreadPoolExecutor(max_workers=10)

    @run_on_executor
    def post(self):
        if self.request.body:
            params = json.loads(self.request.body)
        else:
            params = {}
        text = params.get('text')
        auth_code = params.get('auth_code')
        if auth_code != env.AUTH_CODE:
            self.write(resp_error('参数错误'))
            logger.exception(f"EmbeddingHandler 参数错误 auth_code:{auth_code} ip:{self.request.remote_ip}")
            return
        logger.info(f"start EmbeddingHandler")
        try:
            success, embedding = async_process(text)
            logger.info(f"finish EmbeddingHandler")
            if success:
                self.write(resp_success(embedding))
            else:
                self.write(resp_error())
        except Exception as e:
            logger.exception(f"EmbeddingHandler error {e}")
            self.write(resp_error())
