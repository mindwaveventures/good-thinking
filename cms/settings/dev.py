from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2tjvfgvg*migeqqxtdf0s^vgz1r(f1jb-o0=#w-3!opa=^=@oi'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

PIPELINE['PIPELINE_ENABLED'] = False

try:
    from .local import *
except ImportError:
    pass
