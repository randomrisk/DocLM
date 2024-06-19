#!/usr/bin/env python
# encoding: utf-8

import json
import logging
import env
import glo
import tornado.web
import multiprocessing
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


def async_process(question: str, content: str, model: str):
    process_pool = glo.get_value('process_pool')
    t = process_pool.apply_async(GPT.get_answer, (question, content, model))
    result = None
    try:
        result = t.get(timeout=env.PROCESS_TIMEOUT)
        return True, result
    except multiprocessing.context.TimeoutError:
        logger.error(f"async task process timeout after {env.PROCESS_TIMEOUT}s")
        return False, result
    except Exception as e:
        logger.exception(f"async task process error {e}")
        return False, result


def async_process_summary(context: str, model: str):
    process_pool = glo.get_value('process_pool')
    t = process_pool.apply_async(GPT.get_summary, (context, model))
    result = None
    try:
        result = t.get(timeout=env.PROCESS_TIMEOUT)
        return True, result
    except multiprocessing.context.TimeoutError:
        logger.error(f"async_process_summary timeout after {env.PROCESS_TIMEOUT}s")
        return False, result
    except Exception as e:
        logger.exception(f"async_process_summary error {e}")
        return False, result


def async_process_questions(context: str, model: str):
    process_pool = glo.get_value('process_pool')
    t = process_pool.apply_async(GPT.get_questions, (context, model))
    result = None
    try:
        result = t.get(timeout=env.PROCESS_TIMEOUT)
        return True, result
    except multiprocessing.context.TimeoutError:
        logger.error(f"async_process_questions timeout after {env.PROCESS_TIMEOUT}s")
        return False, result
    except Exception as e:
        logger.exception(f"async_process_questions error {e}")
        return False, result


class QaHandler(BaseHandler):
    """
        问答
    """
    executor = ThreadPoolExecutor(max_workers=10)

    @run_on_executor
    def post(self):
        if self.request.body:
            params = json.loads(self.request.body)
        else:
            params = {}
        question = params.get('question')
        content = params.get('content')
        auth_code = params.get('auth_code')
        model = params.get('model')
        if auth_code != env.AUTH_CODE or model not in ['gpt-3.5-turbo', 'text-curie-001']:
            self.write(resp_error('参数错误'))
            logger.exception(f"QaHandler 参数错误 auth_code:{auth_code} ip:{self.request.remote_ip}")
            return
        logger.info(f"start QA")
        try:
            success, answer = async_process(question, content, model)
            logger.info(f"finish QA")
            if success:
                self.write(resp_success(answer))
            else:
                self.write(resp_error())
        except Exception as e:
            logger.exception(f"QaHandler error {e}")
            self.write(resp_error())


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
        content = params.get('content')
        auth_code = params.get('auth_code')
        model = params.get('model')
        if auth_code != env.AUTH_CODE or model not in ['gpt-3.5-turbo', 'text-curie-001']:
            self.write(resp_error('参数错误'))
            logger.exception(f"SummaryAndQuestionsHandler 参数错误 auth_code:{auth_code} ip:{self.request.remote_ip}")
            return
        try:
            data = {}
            success, summary = async_process_summary(content, model)
            if success:
                data['summary'] = summary
            success, questions = async_process_questions(content, model)
            if success:
                data['questions'] = questions
            self.write(resp_success(data))
        except Exception as e:
            logger.exception(f"SummaryAndQuestionsHandler error {e}")
            self.write(resp_error())
