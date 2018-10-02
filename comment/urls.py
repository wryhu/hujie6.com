# coding=utf-8
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^submit_comment/', views.submit_comment, name='submit_comment'),
    url(r'^submit_reply/', views.submit_reply, name='submit_reply'),
]