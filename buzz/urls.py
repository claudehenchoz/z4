from django.conf.urls import patterns, url

from buzz import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^tagi/$', views.tagi, name='tagi'),
    url(r'^woz/$', views.woz, name='woz'),
    url(r'^rps/$', views.rps, name='rps')
)
