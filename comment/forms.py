# -*- coding: utf-8 -*-
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget


class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    text = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'),
                           error_messages={'required': '评论内容不能为空'}, label=False)

    def __init__(self, *args, **kwargs):
        if kwargs.get('user') is not None:
            self.user = kwargs.pop('user')
        super(CommentForm, self).__init__(*args, **kwargs)

    # 虽然前端已经判断用户是否登录了,但考虑到安全性后端也要判断
    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('为了防止垃圾信息,请您登录后评论')
        # 评论对象是否存在
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']
        try:
            # 通过ContentType模型取出blog对象对应的Blog模型
            model_class = ContentType.objects.get(model=content_type).model_class()
            # 再通过具体id取出blog对象
            model_obj = model_class.objects.get(pk=object_id)
            self.cleaned_data['content_object'] = model_obj
        except ObjectDoesNotExist:
            raise forms.ValidationError('评论对象不存在')

        return self.cleaned_data