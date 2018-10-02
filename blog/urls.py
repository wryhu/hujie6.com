# coding=utf-8
from django.conf.urls import url
from . import views


urlpatterns = [
    # 全部博客,分页,用get请求显示每一页的全部博客,默认?page=1
    url(r'^$', views.blog_list, name='blog_list'),
    # 一篇博客
    url(r'^(\d+)/', views.blog_detail, name='blog_detail'),
    # 分类博客,机制同全部博客,所以模板方面继承即可
    url(r'^type_(\d+)/', views.blogs_by_type, name='blogs_by_type'),
    # 每月博客,机制同全部博客,所以模板方面继承即可
    url(r'^date_(\d+)_(\d+)/', views.blogs_by_date, name='blogs_by_date'),
]