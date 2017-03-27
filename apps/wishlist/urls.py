from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^create_item$', views.create_item, name = 'create_item'),
    url(r'^create$', views.create, name = 'create'),
    url(r'^wish_item/(?P<id>\d+)$', views.wish_item, name = 'wish_item'),
    url(r'^add/(?P<id>\d+)$', views.add, name = 'add'),
    url(r'^remove/(?P<id>\d+)$', views.remove, name = 'remove'),
    url(r'^delete/(?P<id>\d+)$', views.delete, name = 'delete'),
]