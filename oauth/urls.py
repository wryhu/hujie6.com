from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^oauth_login', views.oauth_login, name='oauth_login'),
    url(r'^(qq)_check', views.check, name='qq_check'),
    url(r'^(github)_check', views.check, name='github_check'),
    url(r'^(sina)_check', views.check, name='sina_check'),
    url(r'^(baidu)_check', views.check, name='baidu_check'),
    url(r'^(line)_check', views.check, name='line_check'),
    url(r'^(facebook)_check', views.check, name='facebook_check'),
    url(r'^bind_email', views.bind_email, name='bind_email'),
]