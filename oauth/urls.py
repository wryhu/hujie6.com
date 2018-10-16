from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'qq_login', views.qq_login, name='qq_login'),
    url(r'qq_check', views.qq_check, name='qq_check'),

    url(r'github_login', views.github_login, name='github_login'),
    url(r'github_check', views.github_check, name='github_check'),

    url(r'bind_email', views.bind_email, name='bind_email'),
]