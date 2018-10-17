# coding:utf-8
import json
import urllib, urllib2, urlparse


class OAuth_QQ:
    def __init__(self, client_id, client_key, redirect_uri):
        self.client_id = client_id
        self.client_key = client_key
        self.redirect_uri = redirect_uri

    def get_auth_url(self):
        """获取授权页面的网址"""
        params = {'client_id': self.client_id,
                  'response_type': 'code',
                  'redirect_uri': self.redirect_uri,
                  'scope': 'get_user_info',
                  'state': 1}
        url = 'https://graph.qq.com/oauth2.0/authorize?%s' % urllib.urlencode(params)
        return url

    def get_access_token(self, code):
        """根据code获取access_token"""
        params = {'grant_type': 'authorization_code',
                  'client_id': self.client_id,
                  'client_secret': self.client_key,
                  'code': code,
                  'redirect_uri': self.redirect_uri}
        url = 'https://graph.qq.com/oauth2.0/token?%s' % urllib.urlencode(params)

        # 访问该网址，获取access_token
        response = urllib2.urlopen(url).read()
        # 响应数据转化成字典类型后提取
        result = urlparse.parse_qs(response, True)
        self.access_token = result['access_token'][0]
        return self.access_token

    def get_open_id(self):
        """获取QQ的OpenID"""
        params = {'access_token': self.access_token}
        url = 'https://graph.qq.com/oauth2.0/me?%s' % urllib.urlencode(params)

        response = urllib2.urlopen(url).read()
        v_str = str(response)[9:-3]  # 去掉callback的字符
        v_json = json.loads(v_str)

        self.openid = v_json['openid']
        return self.openid

    def get_nickname(self):
        """获取QQ用户的资料信息"""
        params = {'access_token': self.access_token,
                  'oauth_consumer_key': self.client_id,
                  'openid': self.openid}
        url = 'https://graph.qq.com/user/get_user_info?%s' % urllib.urlencode(params)
        response = urllib2.urlopen(url).read()
        result = json.loads(response)
        return result['nickname']


class OAuth_GITHUB:
    def __init__(self, client_id, client_key, redirect_uri):
        self.client_id = client_id
        self.client_key = client_key
        self.redirect_uri = redirect_uri

    def get_auth_url(self):
        """获取授权页面的网址"""
        params = {'client_id': self.client_id,
                  'response_type': 'code',
                  'redirect_uri': self.redirect_uri,
                  'scope': 'get_user_info',
                  'state': 1}
        url = 'https://github.com/login/oauth/authorize?%s' % urllib.urlencode(params)
        return url

    def get_access_token(self, code):
        print(111111111111111111111111111111111)
        """根据code获取access_token"""
        params = {'grant_type': 'authorization_code',
                  'client_id': self.client_id,
                  'client_secret': self.client_key,
                  'code': code,
                  'redirect_uri': self.redirect_uri}
        url = 'https://github.com/login/oauth/access_token?%s' % urllib.urlencode(params)

        # 访问该网址，获取access_token
        response = urllib2.urlopen(url).read()
        # 响应数据转化成字典类型后提取
        result = urlparse.parse_qs(response, True)
        self.access_token = result['access_token'][0]
        return self.access_token

    def get_open_id(self):
        self.get_nickname()
        return self.open_id

    def get_nickname(self):
        params = {'access_token': self.access_token}
        url = 'https://api.github.com/user?%s' % urllib.urlencode(params)
        response = urllib2.urlopen(url).read()
        result = json.loads(response)
        self.open_id = result.get('id', '')
        return result['login']


class OAuth_SINA:
    def __init__(self, client_id, client_key, redirect_uri):
        self.client_id = client_id
        self.client_key = client_key
        self.redirect_uri = redirect_uri

    def get_auth_url(self):
        """获取授权页面的网址"""
        params = {'client_id': self.client_id,
                  'response_type': 'code',
                  'redirect_uri': self.redirect_uri}
        url = 'https://api.weibo.com/oauth2/authorize?%s' % urllib.urlencode(params)
        return url

    def get_access_token(self, code):
        """根据code获取access_token"""
        params = {'grant_type': 'authorization_code',
                  'client_id': self.client_id,
                  'client_secret': self.client_key,
                  'code': code,
                  'redirect_uri': self.redirect_uri}
        url = 'https://api.weibo.com/oauth2/access_token?%s' % urllib.urlencode(params)
        # 访问该网址，获取access_token
        response = urllib2.urlopen(url).read()
        # 响应数据转化成python类型
        result = json.loads(response)
        self.access_token = result['access_token']
        return self.access_token

    def get_open_id(self):
        pass

    def get_nickname(self):
        """获取QQ用户的资料信息"""
        params = {'access_token': self.access_token,
                  'oauth_consumer_key': self.client_id,
                  'openid': self.openid}
        url = 'https://graph.qq.com/user/get_user_info?%s' % urllib.urlencode(params)

        response = urllib2.urlopen(url).read()
        return json.loads(response)


class OAuth_BAIDU:
    def __init__(self, client_id, client_key, redirect_uri):
        self.client_id = client_id
        self.client_key = client_key
        self.redirect_uri = redirect_uri

    def get_auth_url(self):
        """获取授权页面的网址"""
        params = {'client_id': self.client_id,
                  'response_type': 'code',
                  'redirect_uri': self.redirect_uri}
        url = 'http://openapi.baidu.com/oauth/2.0/authorize?%s' % urllib.urlencode(params)
        return url

    def get_access_token(self, code):
        print(222222222222222222222222)
        """根据code获取access_token"""
        params = {'grant_type': 'authorization_code',
                  'client_id': self.client_id,
                  'client_secret': self.client_key,
                  'code': code,
                  'redirect_uri': self.redirect_uri}
        url = 'https://openapi.baidu.com/oauth/2.0/token?%s' % urllib.urlencode(params)
        # 访问该网址，获取access_token
        response = urllib2.urlopen(url).read()
        # 响应数据转化成python格式
        result = json.loads(response)
        self.access_token = result['access_token']
        return self.access_token

    def get_open_id(self):
        self.get_nickname()
        return self.open_id

    def get_nickname(self):
        params = {'access_token': self.access_token}
        url = 'https://openapi.baidu.com/rest/2.0/passport/users/getInfo?%s' % urllib.urlencode(params)
        response = urllib2.urlopen(url).read()
        result = json.loads(response)
        self.open_id = result['userid']
        return result['username']