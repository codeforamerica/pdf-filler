# -*- coding: utf-8 -*-
import os

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(HERE, os.pardir))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://localhost/')
    SERVER_NAME = os.environ.get('HOST_NAME', 'localhost:5000')


class ProdConfig(Config):
    ENV = 'prod'
    DEBUG = False


class DevConfig(Config):
    ENV = 'dev'
    DEBUG = True
    LOAD_FAKE_DATA = True


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL', 'postgresql://localhost/')
    TESTING = True
    DEBUG = True
    # For: `nose.proxy.AssertionError: Popped wrong request context.`
    # http://stackoverflow.com/a/28139033/399726
    # https://github.com/jarus/flask-testing/issues/21
    PRESERVE_CONTEXT_ON_EXCEPTION = False
