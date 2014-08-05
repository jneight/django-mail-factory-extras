# coding=utf-8

def get_version():
    return '%s.%s' % (VERSION[0], VERSION[1])


VERSION = (0, 23,)

__version__ = get_version()
__author__ = 'Javier Cordero'
__email__ = 'jcorderomartinez@gmail.com'
__license__ = 'Apache 2.0'

from .smsfactory import SMSFactory

smsfactory = SMSFactory()

default_app_config = 'mailfactory_extras.apps.MailFactoryExtrasConfig'
