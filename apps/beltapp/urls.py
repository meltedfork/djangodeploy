from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^success$', views.success),
    url(r'^logout$', views.logout),
    url(r'^new$', views.new),
    url(r'^create$', views.create),
    url(r'^(?P<id>\d+)/favorite$', views.favorite),
    url(r'^(?P<id>\d+)/popback$', views.popback),
    url(r'^(?P<id>\d+)/show$', views.show),
    url(r'^(?P<id>\d+)/remove$', views.remove),
    url(r'^(?P<id>\d+)/delete$', views.destroy),
]