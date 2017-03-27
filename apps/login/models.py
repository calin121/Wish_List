from __future__ import unicode_literals
from django.db import models
from dateutil.parser import parse as parse_date
import re, bcrypt, datetime
from datetime import date

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
	def register_user(self, postData):
		errors = []

		# 1. run our validations
		if len(postData['name']) < 2:
			errors.append('Name must be 2 characters or more!')
		if len(postData['username']) < 2:
			errors.append('Username must be 2 characters or more!')
		if self.filter(username = postData['username']):
			errors.append("This username has already been registered!")
		if not len(postData['email']):
			errors.append('Email is required!')
		else:
			if not EMAIL_REGEX.match(postData['email']):
				errors.append('Enter a valid email!')
		if len(postData['password']) < 8:
			errors.append('Password must be at least 8 characters long!')
		if not postData['password'] == postData['confirm_password']:
			errors.append('Password must match!')
		if postData['hire_date'] == '':
			errors.append('Hire Date must be filled out!')
		else:	
			dt = datetime.datetime.strptime(postData['hire_date'], "%Y-%m-%d").date()
			if dt > datetime.date.today():
					errors.append('Hire Date cannot be a future date!')
	
		response_to_views = {}
		# 2. check if validations are true or false
		# 2a. if true
		if not errors:
			# create user
			hashed_password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
			user = self.create(name = postData['name'], username = postData['username'], email = postData['email'], password = hashed_password, hire_date = postData['hire_date'])
			
			response_to_views['user'] = user
			response_to_views['status'] = True
			response_to_views['confirm'] = ['You just successfully registered!']
				# send a resonse to views (user, true)
			# 2b. if false
		else:
			# send a response to views (errors, false)
			response_to_views['user'] = errors
			response_to_views['status'] = False
		# send response to the views
		return response_to_views

	def login_user(self, postData):
		errors = []
		response_to_views = {}
		# find a user with email for PostData
		user = self.filter(username = postData['username'])
		response_to_views['user'] = user
		# if not user
		if not user:
			# send errors to views
			response_to_views['status'] = False
			errors.append('Username not found!')
			response_to_views['user'] = errors
		# else
		else:
			# check passwords from postData to hashed_password from db
			if bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()): #encode all password before sending and/or checking
			# if true
				response_to_views['status'] = True
				response_to_views['user'] = user.first()
				response_to_views['confirm'] = ['You have successfully logged in!']
				# send user to sucess.views, true

			# if false
			else:
				# send errors to views, false
				response_to_views['status'] = False
				errors.append('Invalid Username/Password combination!')
				response_to_views['user'] = errors
		return response_to_views

class User(models.Model):
	name = models.CharField(max_length = 55)
	username = models.CharField(max_length = 55)
	email = models.CharField(max_length = 255)
	password = models.CharField(max_length = 255)
	hire_date = models.DateField(null=True)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)


	objects = UserManager()