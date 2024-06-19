#!/usr/bin/env python
# encoding: utf-8

import json
import logging
import env
import asyncio
import tornado.web
from openai_api import get_answer_with_role, get_answer_with_context, prompts
from tornado.concurrent import run_on_executor
from concurrent.futures.thread import ThreadPoolExecutor
from auth import decode_chat_data

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


class QaHandler(tornado.web.RequestHandler):
    """
        问答
    """

    executor = ThreadPoolExecutor(max_workers=10)

    @run_on_executor()
    def post(self):
        try:
            asyncio.get_event_loop()
        except Exception as e:
            logger.info('QaHandler set loop')
            asyncio.set_event_loop(asyncio.new_event_loop())

        if self.request.body:
            params = json.loads(self.request.body)
        else:
            params = {}
        question = params.get('question')
        context = params.get('context')
        auth_code = params.get('auth_code')
        model = params.get('model')
        self.add_header("X-Accel-Buffering", "no")
        if auth_code != env.AUTH_CODE or model not in ['gpt-3.5-turbo', 'text-curie-001']:
            logger.exception(f"QaHandler 参数错误 auth_code:{auth_code} ip:{self.request.remote_ip}")
            self.finish()
            return
        try:
            for answer in get_answer_with_context(question, context, model):
                if answer:
                    self.write(answer)
                    self.flush()
            self.finish()
        except Exception as e:
            logger.exception(f"QaHandler error {e}")
            self.finish()


class QaWithRoleHandler(tornado.web.RequestHandler):
    """
        问答
    """

    executor = ThreadPoolExecutor(max_workers=10)

    @run_on_executor()
    def post(self):
        try:
            asyncio.get_event_loop()
        except Exception as e:
            logger.info('QaWithRoleHandler set loop')
            asyncio.set_event_loop(asyncio.new_event_loop())

        if self.request.body:
            params = json.loads(self.request.body)
        else:
            params = {}
        question = params.get('question')
        role = params.get('role')
        auth_code = params.get('auth_code')
        self.add_header("X-Accel-Buffering", "no")
        self.add_header("Content-Type", "text/event-steam")
        self.add_header("Cache-Control", " no-cache")
        self.add_header("Connection", "keep-alive")

        if auth_code != env.AUTH_CODE or role not in prompts:
            logger.exception(
                f"QaWithRoleHandler 参数错误 auth_code:{auth_code} role:{role} ip:{self.request.remote_ip}")
            self.finish()
            return
        try:
            for answer in get_answer_with_role(question, role):
                if answer:
                    self.write(answer)
                    self.flush()
            self.finish()
        except Exception as e:
            logger.exception(f"QaWithRoleHandler error {e}")
            self.finish()


class QaWithTokenHandler(tornado.web.RequestHandler):
    """
        问答
    """

    executor = ThreadPoolExecutor(max_workers=10)

    @run_on_executor()
    def post(self):
        try:
            asyncio.get_event_loop()
        except Exception as e:
            logger.info('QaWithTokenHandler set loop')
            asyncio.set_event_loop(asyncio.new_event_loop())
        try:
            self.add_header("X-Accel-Buffering", "no")
            # self.add_header("Content-Type", "text/event-steam")
            # self.set_header("Content-Type", "application/json; charset=UTF-8")
            # self.add_header("Cache-Control", " no-cache")
            # self.add_header("Connection", "keep-alive")
            if self.request.body:
                params = json.loads(self.request.body)
            else:
                params = {}
            token = params.get('token')
            success, data = decode_chat_data(token)
            logger.info(f"QaWithTokenHandler {success} {data}")
            if not success:
                self.write('token error')
                self.finish()
                return
            role = data.get('role')
            question = data.get('question')
            if role not in prompts:
                self.write('role error')
                self.finish()
                return
            for answer in get_answer_with_role(question, role):
                if answer:
                    self.write(answer)
                    self.flush()
            self.finish()
        except Exception as e:
            logger.exception(f"QaWithRoleHandler error {e}")
            self.finish()
