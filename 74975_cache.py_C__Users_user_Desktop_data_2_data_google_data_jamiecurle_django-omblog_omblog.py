from django.conf import settings as django_settings
from omblog import settings as omblog_settings


def get_key(key):
    try:
        django_prefix = django_settings.CACHES['default']['KEY_PREFIX']
    except KeyError:
        django_prefix = ''
    return '%s_%s_%s' % (django_prefix, omblog_settings.CACHE_PREFIX, key)
