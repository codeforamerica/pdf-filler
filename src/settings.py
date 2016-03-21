# -*- coding: utf-8 -*-
import os

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(HERE, os.pardir))
DEFAULT_DATABASE_PATH = 'sqlite:///' + os.path.join(PROJECT_ROOT, 'data', 'default.db')
DEFAULT_TEST_DATABASE_PATH = 'sqlite:///' + os.path.join(PROJECT_ROOT, 'data', 'test_default.db')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', DEFAULT_DATABASE_PATH)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    ENV = 'prod'
    DEBUG = False
    PREFERRED_URL_SCHEME = 'https'


class DevConfig(Config):
    ENV = 'dev'
    DEBUG = True
    LOAD_FAKE_DATA = True


class TestConfig(Config):
    ENV = 'test'
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL', DEFAULT_TEST_DATABASE_PATH)
    TESTING = True
    DEBUG = True
