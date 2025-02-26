# -*- coding: utf-8 -*-
#
#  @Author: Walter Schreppers
#
#  app/config.py
#
#   configuration per environment
#

import os


def flask_environment():
    env = os.environ.get('FLASK_ENV', 'DEVELOPMENT')
    configs = {
        'TESTING': 'app.config.TestConfig',
        'DEVELOPMENT': 'app.config.DevConfig',
        'PRODUCTION': 'app.config.PrdConfig',
    }

    return configs[env]


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    # SECRET_KEY = 'somesecret_key_here234232425223faifaf'
    UPLOAD_FOLDER = 'subtitle_uploads'


class PrdConfig(Config):
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = False


class TestConfig(Config):
    DEVELOPMENT = True
    DEBUG = False
    TESTING = True
