# coding=utf-8
from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


# 建立各种表单并增加验证用户信息功能(原生表单只验证字符格式)
# 登录的表单
class LoginForm(forms.Form):
    username = forms.CharField(label='用户名',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': u'请输入用户名'}))
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': u'请输入密码'}))

    # 验证用户是否为我站注册用户
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError(u'用户名或密码错误')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


# 注册的表单
class RegForm(forms.Form):
    username = forms.CharField(label='用户名',
                               max_length=20,
                               min_length=3,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': u'请输入3-20位字符'}))
    email = forms.CharField(label='邮箱',
                            widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': u'请输入邮箱'}))
    password = forms.CharField(label='密码',
                               min_length=6,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': u'请输入密码'}))
    password_again = forms.CharField(label='确认密码',
                                     widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': u'再次输入密码'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次输入的密码不一致')
        return password_again