import os
import env
import logging.config

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '{asctime} {levelname} {process} {threadName} {name}:{lineno} {message}',
            'style': '{',
        }
    },
    'handlers': {
        'file': {
            'level': env.LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(env.LOG_DIR, "log.log"),  # 日志文件
            'maxBytes': 1024 * 1024 * 100,  # 日志大小 100M
            'backupCount': 3,  # 最多备份几个
            'formatter': 'simple',
            'encoding': 'utf-8',
        },
        'console': {
            'level': env.LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        }
    },
    'loggers': {
        # 默认的logger应用如下配置
        '': {
            'handlers': ['console', 'file'],
            'level': env.LOG_LEVEL,
            'propagate': True,  # 向不向更高级别的logger传递
        }
    }
}


def init_basic_logger():
    logging.config.dictConfig(LOGGING)
