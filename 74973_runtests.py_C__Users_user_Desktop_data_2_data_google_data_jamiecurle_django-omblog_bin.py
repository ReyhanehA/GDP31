#!/usr/bin/env python
import os
import sys

from django.conf import settings

DIRNAME = os.path.dirname(__file__)

settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
    ROOT_URLCONF='omblog.tests.urls',
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
        'omblog',
        'django_nose',
    ),
    NOSE_ARGS = [
        '--with-coverage',
        '--cover-package=omblog',
        '--cover-xml',
        '--verbosity=2',
    ],
)

from django_nose import NoseTestSuiteRunner

test_runner = NoseTestSuiteRunner(verbosity=1)

failures = test_runner.run_tests(['omblog'])

if failures:
    sys.exit(failures)
