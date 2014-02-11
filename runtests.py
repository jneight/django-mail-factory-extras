#!/usr/bin/env python
import sys
import os
from django.conf import settings

TEST_ROOT = os.path.realpath(os.path.dirname(__file__))
RUNTESTS_DIR = os.path.join(TEST_ROOT, 'tests')

sys.path.insert(0, TEST_ROOT)
sys.path.insert(0, RUNTESTS_DIR)

settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'test',
            'USER': '',
            'PASSWORD': '',
        }
    },
    INSTALLED_APPS=(
        'mail_factory',
        'mailfactory_extras',
        'tests',
    ),
    USE_TZ=True,
)

def get_test_modules():
    modules = []
    for f in os.listdir(RUNTESTS_DIR):
        if (f.startswith('__init__') or
            f.startswith('.') or
            f.startswith('sql') or not os.path.isdir(os.path.join(RUNTESTS_DIR, f))):
            continue
        modules.append(f)
    return modules

from django.test.utils import get_runner
test_runner = get_runner(settings)(verbosity=1)
failures = test_runner.run_tests(['tests.mails'])
if failures:
    sys.exit(failures)
