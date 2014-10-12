# coding=utf-8

try:
    from django.apps import AppConfig
except ImportError:
    AppConfig = object

class MailFactoryExtrasConfig(AppConfig):
    name = 'mailfactory_extras'
    verbose = 'MailFactory extras'

