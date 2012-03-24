from celery.task import task
import urllib
import re
import os
import random
from utils import create_file_directories, hashfile, b58encode
from models import File
from settings import DEBUG
from models import get_setting, set_setting

API_URL="http://localhost:7999"

def call_api(url_suffix, data = None):
    if DEBUG:
        print "Calling URL: "+API_URL + url_suffix
        return None
    else:
        f = urllib.urlopen(API_URL + url_suffix, data)
        data = f.read()
        print data
        return json.loads(data)

@task()
def file_download(uuid, url, filename, expires_at):
    print "task executing", url
    print "filename", filename
    file_dir = create_file_directories(uuid)
    print "file_dir", file_dir
    #uuid_filename
    file_path = file_dir+"/"+filename
    urllib.urlretrieve(url, file_path)
    sha256_hash = hashfile(file_path)
    f=File.objects.create(uuid=uuid, name=filename, file_sha256=sha256_hash)
    f.save()
    call_api("/file_downloaded/"+uuid+"/"+sha256_hash)
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
