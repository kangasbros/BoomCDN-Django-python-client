from django.db.models.signals import post_syncdb
import files.models
from files.tasks import generate_test_file
from settings import username, profile_uuid, SERVER_URL, clientserver_ip, clientserver_port
import hashlib
import urllib
import re
import os
import random
from django.utils import simplejson

def call_api(url_suffix, data = None):
    f = urllib.urlopen(SERVER_URL + url_suffix, data)
    data = f.read()
    print data, type(data)
    return simplejson.loads(data)

def initialize_db(sender, **kwargs):
    # Your specific logic here
    if files.models.get_setting("server_uuid"):
        print "server uuid already exists!"
        return
    print "Generating test file..."
    generate_test_file()
    f=files.models.File.objects.get(id=int(files.models.get_setting("test_file")))
    print "File generated, uuid", f.uuid, f.name
    file_id=int(files.models.get_setting("test_file"))
    # call NEW_SERVERCLIENT
    # set server_uuid=get_setting("server_uuid")
    data={
        "username": username,
        "ip_address": clientserver_ip,
        "port": clientserver_port,
        'test_file_hash': f.file_sha256,
        'test_file_uuid': f.uuid,
    }
    to_hash = '%s%s%s%s%s%s' % (data["username"], data["ip_address"], data["port"], data["test_file_uuid"],\
        data["test_file_hash"], profile_uuid)
    test_hash = hashlib.sha256(to_hash).hexdigest()
    data['sign_key_profile'] = test_hash
    results=call_api("/clientserver/new", urllib.urlencode(data))
    print "new server registered", results
    files.models.set_setting("server_uuid", results["data"])
    print "server uuid", files.models.get_setting("server_uuid")

post_syncdb.connect(initialize_db, sender=files.models)
