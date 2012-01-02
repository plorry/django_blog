from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from gallery.models import Gallery
from calendar.models import Calendar

class Blog_Site(models.Model):
	title = models.CharField(max_length = 50)
	calendar = models.ForeignKey(Calendar)	

class Blog(models.Model):
	author = models.ForeignKey(User)
	title = models.CharField(max_length = 50)
	body = models.TextField(max_length = None)
	blog = models.ForeignKey(Blog_Site)
	#tags = models.ManyToManyField('Tag', blank=True, null=True)
	creation_date = models.DateTimeField(auto_now_add = True)
	modified = models.DateTimeField(auto_now = True, blank = True, null = True)
	gallery = models.ForeignKey(Gallery, blank = True, null = True)
	comments = models.ManyToManyField('Comment', blank = True, null = True)
	published = models.BooleanField(default = False)
	def save(self, *args, **kwargs):
		if not self.id:
			self.creation_date = datetime.datetime.today()
		self.modified = datetime.datetime.today()
		super(User, self).save(*args, **kwargs)
	
	def __unicode__(self):
		return self.title
	
class Comment(models.Model):
	author = models.CharField(max_length = 50)
	email = models.EmailField(blank = True, null = True)
	creation_date = models.DateTimeField(auto_now_add = True)
	body = models.TextField(max_length = None)