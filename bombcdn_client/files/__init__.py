from django.db.models.signals import post_syncdb
import files.models
from files.tasks import generate_test_file
import settings import username, user_uuid

def call_api(url_suffix, data = None):
    if DEBUG:
        print "Calling URL: "+API_URL + url_suffix
        return None
    else:
        f = urllib.urlopen(API_URL + url_suffix, data)
        data = f.read()
        print data
        return json.loads(data)

def initialize_db(sender, **kwargs):
    # Your specific logic here
    print "Generating test file..."
    generate_test_file()
    f=files.models.File.objects.get(id=int(files.models.get_setting("test_file")))
    print "File generated, uuid", f.uuid, f.name
    id=int(files.models.get_setting("server_uuid"))
    # call NEW_SERVERCLIENT
    # set server_uuid=get_setting("server_uuid")
    

post_syncdb.connect(initialize_db, sender=files.models)