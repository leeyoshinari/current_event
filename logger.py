#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari

import os
log_path = 'logs'
if not os.path.exists(log_path):
    os.mkdir(log_path)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(asctime)s - %(levelname)s - [%(threadName)s:%(thread)d] - %(filename)s[line:%(lineno)d] - %(message)s",
            "use_colors": None,
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.handlers.RotatingFileHandler",
            'filename': os.path.join(log_path, "access.log"),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 3,
            'encoding': 'utf-8',
        },
        "access": {
            "formatter": "default",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["default"],
            "level": "INFO",    # DEBUG、INFO、WARNING、ERROR、CRITICAL
            "propagate": True
        }
    },
}