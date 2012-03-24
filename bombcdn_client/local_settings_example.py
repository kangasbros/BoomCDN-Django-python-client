# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from settings import DATABASES

import os

HOME = os.environ['HOME']

DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
DATABASES['default']['NAME'] = 'bombcdn_client.db'

username="" # your boomcdn username
profile_uuid="KKb1TGTmmqMK2XKYM34kzc" # your boomcdn secret key
clientserver_ip="178.73.194.178" # your ip address
clientserver_port=8000 # your listening port

DEBUG = True

ADMINS = (
    ('BombCDN', 'bombcdn+client@bombcdn.com')
)

MEDIA_ROOT = os.path.join(HOME, 'src', 'git_checkouts', 'bombcdn_client', 'media')

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# EOF

