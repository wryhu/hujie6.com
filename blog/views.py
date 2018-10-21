# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Blog, BlogType
from django.db.models import Count
from read_count.utils import read_count_func
from django.contrib.contenttypes.models import ContentType
from comment.models import Comment
from comment.forms import CommentForm
# 定义每一页显示的博客数量
numbers_of_onepage = 4


# 这是博客列表页,分类页,日期归档页的代码重用部分
def blog_common_data(request, blogs):
    # 建立分页器对象
    paginator = Paginator(blogs, numbers_of_onepage)
    # 获取GET请求参数
    page_num = request.GET.get('page', 1)
    try:
        page_of_blogs = paginator.page(page_num)
    except PageNotAnInteger:
        # 如果page不是一个整数，则展示第一页。
        page_of_blogs = paginator.page(1)
    except EmptyPage:
        # 如果page不在范围内（例如，9999），则展示结果的最后一页。
        page_of_blogs = paginator.page(1)
    # 优化分页显示
    current_page = page_of_blogs.number
    page_range = range(max(current_page - 2, 1), current_page) + \
                 range(current_page, min(current_page + 2, paginator.num_pages) + 1)
    # 添加省略号
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 添加首尾页码
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    # 建立每月的文章数的字典
    blog_dates_dict = {}
    blog_dates = Blog.objects.dates('created_time', 'month', order="DESC")
    for blog_date in blog_dates:
        blog_dates_dict[blog_date] = Blog.objects.filter(created_time__year=blog_date.year,
                                     created_time__month=blog_date.month).count()
    context = {}
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['page_range'] = page_range
    context['blog_dates'] = blog_dates_dict
    blogs_random = Blog.objects.exclude(id=0).order_by('?')[:10]
    context['blogs_random'] = blogs_random
    return context


# 全部博客
def blog_list(request):
    # 获取博客集合
    blogs = Blog.objects.all()
    context = blog_common_data(request, blogs)

    return render(request, 'blog/blog_list.html', context)


# 单个分类的博客
def blogs_by_type(request, blogs_by_type):
    blog_type = get_object_or_404(BlogType, pk=blogs_by_type)
    blogs = Blog.objects.filter(blog_type=blog_type)
    context = blog_common_data(request, blogs)
    context['blog_type'] = blog_type
    return render(request, 'blog/blogs_by_type.html', context)


# 每年每月的博客
def blogs_by_date(request, year, month):
    blogs = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = blog_common_data(request, blogs)
    context['date_of_blogs'] = "%s年%s月" % (year, month)
    return render(request, 'blog/blogs_by_date.html', context)


# 单个博客
def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    # 独立的处理阅调用读量功能的应用的内部方法
    key = read_count_func(request, blog)
    blog_contenttype = ContentType.objects.get_for_model(model=blog)
    comments = Comment.objects.filter(content_type= blog_contenttype, object_id=blog_pk, parent=None)

    context = {}
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog'] = blog
    context['comments'] = comments
    context['comment_form'] = CommentForm(initial={'content_type': 'blog', 'object_id': blog_pk})
    response = render(request, 'blog/blog_detail.html', context)
    response.set_cookie(key, 'true', max_age=3600)
    return response


# 搜索框，文章标题
def search(request):
    try:
        wd = request.GET['wd']
        if not wd:
            return render(request, 'jojo.html')
        # icontains不区分大小写包含
        blogs = Blog.objects.filter(title__icontains=wd)
        context = blog_common_data(request, blogs)
        context['wd'] = wd
    except Exception:
        return render(request, 'jojo.html')
    return render(request, 'blog/blogs_search.html', context)