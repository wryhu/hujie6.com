from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'oauth_login', views.oauth_login, name='oauth_login'),
    url(r'qq_check', views.check, name='qq_check'),

    url(r'github_check', views.check, name='github_check'),

    url(r'sina_check', views.check, name='sina_check'),

    url(r'baidu_check', views.check, name='baidu_check'),

    url(r'bind_email', views.bind_email, name='bind_email'),
]