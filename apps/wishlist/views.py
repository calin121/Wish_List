from django.shortcuts import render, redirect, HttpResponse
from .models import Product
from ..login.models import User
from django.contrib import messages

# Create your views here.

def index(request):
	pass

def create_item(request):
	if 'user_id' in request.session:
		return render(request, 'wishlist/index.html')
	else:
		return redirect('users:index')

def create(request):
	if 'user_id' in request.session:
		if request.method == 'POST':
			# Create the product in the database
			creator = User.objects.get(id = request.session['user_id'])
			product = request.POST['product']
			description = request.POST['description']
			product = Product.objects.create(description = description, product = product,  creator = creator)
			# Product.objects.create(description = request.POST['description'],course = course, describer = creator)
			

			return redirect('users:success')
	else:
		return redirect('users:index')

def wish_item(request, id):
	if 'user_id' in request.session:

		context = {
			'items_list': Product.objects.filter(id = id),
		}

		return render(request, 'wishlist/wish_item.html', context)
	else:
		return redirect('users:index')

def add(request, id):
	if 'user_id' in request.session:
		if request.method == 'POST':

			# Add item to my wish list
			user = User.objects.get(id = request.session['user_id'])
			product = Product.objects.get(id = id)
			product.all_lists.add(user)

			return redirect('users:success')

def remove(request, id):
	if 'user_id' in request.session:
		# Add item to my wish list
		user = User.objects.get(id = request.session['user_id'])
		product = Product.objects.get(id = id)
		product.all_lists.remove(user)

		return redirect('users:success')

def delete(request, id):
	if 'user_id' in request.session:
		# Delete the item/product
		Product.objects.get(id = id).delete()

		return redirect('users:success')


