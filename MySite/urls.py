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
from django.views.defaults import permission_denied

urlpatterns = [
    url(r'^music$', views.music, name='music'),
    url(r'^$', views.frame, name='frame'),
    url(r'^main$', views.main, name='main'),
    url(r'^home$', views.home, name='home'),
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
    url(r'^ajax_img_crwaler$', views.ajax_img_crwaler, name='ajax_img_crwaler'),
    url(r'^privacy_policy$', views.privacy_policy, name='privacy_policy'),
    url(r'^move$', views.move, name='move'),
    url(r'^translate', views.translate, name='translate'),
    url(r'^mobile', views.mobile, name='mobile'),
    url(r'^frames', views.frames, name='frames'),
    url(r'^xiaoxin', views.xiaoxin, name='xiaoxin'),
    url(r'^online$', views.online, name='online'),
    url(r'^tongJi$', views.tongJi, name='tongJi'),
    url(r'^wx', views.wx, name='wx'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
