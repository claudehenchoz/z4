from django.conf.urls import patterns, url

from buzz import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)
