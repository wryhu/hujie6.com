# encoding=utf8
"""MySite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    # 网站主页
    url(r'^main$', views.main, name='main'),
    url(r'^music$', views.music, name='music'),
    url(r'^$', views.frame, name='frame'),
    url(r'^index$', views.home, name='home'),
    # 管理员页
    url(r'^admin/', admin.site.urls),
    # 转入博客主体相关
    url(r'^blog/', include('blog.urls')),
    url(r'^comment/', include('comment.urls')),
    url(r'^login/', views.login, name='login'),
    url(r'^register/', views.register, name='register'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^jojo/', views.jojo, name='jojo'),
    url(r'^oauth/', include('oauth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
