from celery.task import task
import urllib
import re
import os
import random
import json
from utils import create_file_directories, hashfile, b58encode
from models import File
from settings import username, profile_uuid, SERVER_URL, clientserver_ip, clientserver_port
from models import get_setting, set_setting
import hashlib

def call_api(url_suffix, data = None):
    f = urllib.urlopen(SERVER_URL + url_suffix, data)
    data = f.read()
    print data
    return json.loads(data)

@task()
def file_download(uuid, url, filename, expires_at):
    print "task executing", url
    print "filename", filename
    server_uuid=get_setting("server_uuid")
    file_dir = create_file_directories(uuid)
    print "file_dir", file_dir
    #uuid_filename
    file_path = file_dir+"/"+filename
    urllib.urlretrieve(url, file_path)
    sha256_hash = hashfile(file_path)
    f=File.objects.create(uuid=uuid, name=filename, file_sha256=sha256_hash)
    f.save()
    data={
        "username": username,
        "ip_address": clientserver_ip,
        'file_uuid': uuid,
        'file_hash': sha256_hash,
    }
    to_hash = 'FILE_DOWNLOADED%s%s%s%s' % (data["ip_address"], data["file_uuid"], data["file_hash"], server_uuid)
    test_hash = hashlib.sha256(to_hash).hexdigest()
    print (data["ip_address"], data["file_uuid"], data["file_hash"], server_uuid)
    print to_hash, test_hash
    data['sign_key_clientserver'] = test_hash
    results=call_api("/clientserver/file_downloaded", urllib.urlencode(data))
    print results
    return uuid+url

def generate_test_file():
    filename="test.dat"
    uuid=b58encode(os.urandom(16))
    file_dir = create_file_directories(uuid)
    file_path = file_dir+"/"+filename
    file_size=1024
    fh = open(file_path, 'w')
    while os.path.getsize(file_path) <= file_size:
        fh.write(os.urandom(16))
    fh.close()
    sha256_hash = hashfile(file_path)
    f=File.objects.create(uuid=uuid, name=filename, file_sha256=sha256_hash)
    f.save()
    set_setting("test_file", str(f.id))
    pass

