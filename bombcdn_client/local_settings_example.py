# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from settings import DATABASES

import os

HOME = os.environ['HOME']

DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
DATABASES['default']['NAME'] = 'bombcdn_client.db'

DEBUG = True

ADMINS = (
    ('BombCDN', 'bombcdn+client@bombcdn.com')
)

MEDIA_ROOT = os.path.join(HOME, 'src', 'git_checkouts', 'bombcdn_client', 'media')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# EOF

