#!/usr/bin/env python
# encoding: utf-8

import os

PORT = 80
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.getenv("LOG_DIR", "/work")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
AUTH_CODE = os.getenv("AUTH_CODE", "")
PROCESS_TIMEOUT = int(os.getenv("PROCESS_TIMEOUT", 60))
OPENAI_KEYS = os.getenv("OPENAI_KEYS", "").split('|')
