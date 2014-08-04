# coding=utf-8

try:
    from django.apps import AppConfig
except ImportError:
    AppConfig = object

class MailFactoryExtrasConfig(AppConfig):
    name = 'django_mailfactory_extras'
    verbose = 'Django MailFactory extras'

