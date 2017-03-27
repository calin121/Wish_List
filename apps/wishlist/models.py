from __future__ import unicode_literals
from django.db import models
from ..login.models import User

# Create your models here.

class Product(models.Model):

	product = models.CharField(max_length = 100)
	description = models.TextField(max_length = 1000)
	creator = models.ForeignKey(User, related_name = 'product_creator')
	all_lists = models.ManyToManyField(User, related_name="all_items")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True) 