from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class url_map(models.Model):
	url=models.CharField(max_length=100000)
	short_url=models.CharField(max_length=1000)
	created_by=models.CharField(max_length=100)
	allowed_users=ArrayField(models.CharField(max_length=100), blank=True,null=True,default=[])
	visits=models.IntegerField(default=0)
	expiry=models.IntegerField(default=10)
	date_time_stamp=models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.url
