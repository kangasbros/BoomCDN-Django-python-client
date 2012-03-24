from django.db import models
import datetime
import os
from utils import return_file_directory, create_file_directories

# Create your models here.

class Setting(models.Model):
	"""different options"""
	
	key = models.CharField(max_length=100)
	value = models.CharField(max_length=512)

	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __unicode__(self):
		return u"Settings"

def get_setting(key):
	try:
		s=Setting.objects.get(key=key)
	except Setting.DoesNotExist:
		return None
	return s.value

def set_setting(key, value):
	try:
		s=Setting.objects.get(key=key)
	except Setting.DoesNotExist:
		s=Setting.objects.create(key=key, value=value)
		s.save()
		return True
	s.value=value
	s.save()
	return True

class File(models.Model):
	"""file class"""
	created_at = models.DateTimeField(default=datetime.datetime.now)
	updated_at = models.DateTimeField(default=datetime.datetime.now)

	uuid = models.CharField(max_length=30)
	file_sha256 = models.CharField(max_length=128)
	name = models.CharField(max_length=256)
	expires_at = models.DateTimeField(null=True, default=None)

	alias_to = models.ForeignKey('File', null=True)

	def remove_file(self):
		# first delete all aliases
		for alias in File.objects.filter(alias_to=self):
			alias.remove_file()
		os.remove(return_file_directory(self.uuid))
		self.delete()

	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __unicode__(self):
		return u"File"

def create_alias(old_file, new_uuid, lifetime=None, name=None):
    """Create a new "copy"
    """

    if not name:
    	name=old_file.name

    expires_at=None
    if lifetime:
    	expires_at=(datetime.datetime.now()+datetime.timedelta(seconds=int(lifetime)))

    new_file=File.objects.create(uuid=new_uuid, file_sha256=file.file_sha256, name=name, expires_at=expires_at)

    orig_file_path=return_file_directory(old_file.uuid)+"/"+old_file.name
    new_file_path=create_file_directories(new_file.uuid)+"/"+new_file.name

    os.symlink(orig_file_path, new_file_path)

    new_file.save()

    return new_file
