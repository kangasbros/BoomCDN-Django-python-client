# Create your views here.

from files.tasks import file_download
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
import os
import hashlib
from utils import b58encode, b58decode
from models import File, get_setting, set_setting, create_alias
import sys, traceback
from django.views.decorators.csrf import csrf_exempt

def print_traceback(func):
	def wrap(*args, **kwargs):
		try:
			print "kakka"
			results = func(*args, **kwargs)
			print results
			return results
			print "kakka2"
		except:
			print "Exception in user code:"
	        print '-'*60
	        traceback.print_exc(file=sys.stdout)
	        print '-'*60
	return wrap

@csrf_exempt
@print_traceback
def add_file(request):
	server_uuid=get_setting("server_uuid")
	if request.method == "POST":
		uuid=request.POST["uuid"]
		sign_key_clientserver=request.POST["sign_key_clientserver"]
		url=request.POST["url"]
		filename=request.POST["filename"]
		expires_at=request.POST["expires_at"]
		# to_hash = 'ADD_FILE%s%s%s' % (file_uuid, url, server_uuid)
		to_hash = '%s%s%s%s' % ("ADD_FILE", uuid, url, server_uuid)
		print ("ADD_FILE", uuid, url, server_uuid), to_hash
		test_hash = hashlib.sha256(to_hash).hexdigest()
		if sign_key_clientserver!=test_hash:
			return HttpResponse('{"successful": false, "error": "signature invalid"}')
		file_download.delay(uuid, url, filename, expires_at)
		return HttpResponse('{"successful": true}')
	return HttpResponse('{"successful": false, "error": "wrong request method"}')

@csrf_exempt
@print_traceback
def alias(request):
	server_uuid=get_setting("server_uuid")
	if request.method == "POST":
		uuid=request.POST["uuid"]
		new_uuid=request.POST["new_uuid"]
		lifetime=request.POST["lifetime"]
		sign_key_clientserver=request.POST["sign_key_clientserver"]
		to_hash = '%s%s%s%s%s' % ("ALIAS", uuid, new_uuid, lifetime, server_uuid)
		test_hash = hashlib.sha256(to_hash).hexdigest()
		if sign_key_clientserver!=test_hash:
			return HttpResponse('{"successful": false, "error": "signature invalid"}')
		try:
			original=File.objects.get(uuid=uuid)
			file_alias=create_alias(original, new_uuid, lifetime)
			return HttpResponse('{"successful": true}')
		except File.DoesNotExist:
			return HttpResponse('{"successful": false, "error": "file with that uuid not found"}')
	return HttpResponse('{"successful": false, "error": "wrong request method"}')

@csrf_exempt
@print_traceback
def delete(request):
	server_uuid=get_setting("server_uuid")
	if request.method == "POST":
		uuid=request.POST["uuid"]
		sign_key_clientserver=request.POST["sign_key_clientserver"]
		to_hash = '%s%s%s%s' % ("DELETE", uuid, server_uuid)
		test_hash = hashlib.sha256(to_hash).hexdigest()
		if sign_key_clientserver!=test_hash:
			return HttpResponse('{"successful": false, "error": "signature invalid"}')
		try:
			original=File.objects.get(uuid=uuid)
			original.remove_file()
		except File.DoesNotExist:
			return HttpResponse('{"successful": false, "error": "file with that uuid not found"}')
	return HttpResponse('{"successful": false, "error": "wrong request method"}')
