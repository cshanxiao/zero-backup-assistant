import logging
import logging.config
import os

LOG_PATH = "./logs"
LOG_FILENAME = "default.log"
LOG_LEVEL = logging.INFO
LOG_MAX_BYTES = 64 * 1024 * 1024
LOG_BACKUP_COUNT = 5

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': "%(asctime)s,%(msecs)03d %(levelname)s %(name)s %(message)s (%(filename)s:%(lineno)s)",
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'detail': {
            # %(module)s: 打印日志的当前模块
            # %(funcName)s: 打印日志的当前函数
            'format': "%(asctime)s,%(msecs)03d %(levelname)s %(name)s %(message)s "
                      "(%(filename)s:%(lineno)s %(module)s:%(funcName)s) "
                      "(%(process)d:%(processName)s %(thread)d:%(threadName)s)",
            'datefmt': '%Y-%m-%d %H:%M:%S',
        }
    },
    'handlers': {
        'console': {"level": "INFO",
                    "class": "logging.StreamHandler",
                    "formatter": "standard"
                    },
        'console_detail': {"level": "INFO",
                           "class": "logging.StreamHandler",
                           "formatter": "detail"
                           },
        'rotating': {"class": "logging.handlers.RotatingFileHandler",
                     "filename": os.path.join(LOG_PATH, LOG_FILENAME),
                     "encoding": "utf-8",
                     "maxBytes": LOG_MAX_BYTES,  # 最大日志体积，单位：字节
                     "backupCount": LOG_BACKUP_COUNT,  # 备份日志文件数量
                     "formatter": "standard"
                     },
        'rotating_detail': {"class": "logging.handlers.RotatingFileHandler",
                            "filename": os.path.join(LOG_PATH, LOG_FILENAME),
                            "encoding": "utf-8",
                            "maxBytes": LOG_MAX_BYTES,  # 最大日志体积，单位：字节
                            "backupCount": LOG_BACKUP_COUNT,  # 备份日志文件数量
                            "formatter": "detail"
                            }
    },
    'loggers': {
        'console_logger': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': False
        },
        'console_detail_logger': {
            'handlers': ['console_detail'],
            'level': LOG_LEVEL,
            'propagate': False
        },
        'rotating_logger': {
            'handlers': ['rotating'],
            'level': LOG_LEVEL,
            'propagate': False
        },
        'rotating_detail_logger': {
            'handlers': ['rotating_detail'],
            'level': 'INFO',
            'propagate': False
        },
        'global_logger': {
            'handlers': ['console', 'rotating'],
            'level': LOG_LEVEL,
            'propagate': False
        }
    },
    "root": {
        "handlers": ["console", "rotating"],
        "level": LOG_LEVEL,
        "propagate": False
    }
}


def setup_logging(log_path=LOG_PATH):
    if not os.path.exists(log_path):
        os.mkdir(log_path)

    logging.config.dictConfig(LOGGING_CONFIG)


setup_logging()
logger = logging.getLogger("assistant")

if __name__ == '__main__':
    setup_logging()
    logger = logging.getLogger("console_detail_logger")
    for i in range(10):
        logger.info("x" * 32)
