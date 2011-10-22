#! /usr/bin/env python
# coding:utf-8

import time, random
import urllib, urllib2

# 自作signatureモジュール
import signature

class OAuth:
    def __init__(self, consumer_key, consumer_secret, oauth_token, oauth_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret

def parameter_urlencode(param):
    '''
    param :: dictionary
    辞書の要素をURLエンコードーする
    '''
    return dict(map(lambda pair: map(lambda x:urllib.quote(x, ""), pair), param.items()))

#def concat_param(pair):
#    return '='.join(pair)
    
def concat_header(pair):
    return '%s="%s"' % (pair[0], pair[1])


def oauth_header(param):
    return 'OAuth %s' % ', '.join(map(concat_header, sorted(param.items())))

# OAuthリクエストの作成
def oauth_request(oauth, url, method, param, data, content_type='application/x-www-form-urlencoded'):
    '''
    oauth :: OAuth
    url :: Unicode
    method :: Unicode
    param :: distionary
    data :: dictionary <- ポストするときに使う

    signatureの作成にはdataを追加して作成する
    URLにはparamをクエリとして追加する
    POSTデータにはdataを使う
    '''
    # 乱数の生成
    nonce = str(random.getrandbits(64))
    #システム時間の取得
    unix_time = str(int(time.time()))
    #データをエンコードする
    param_sub = parameter_urlencode(data)
    param_sub.update(parameter_urlencode(param))
    #パラメータ(エンコードしたもの)
    oauth_param = parameter_urlencode(
                  {'oauth_consumer_key': oauth.consumer_key,
                   'oauth_nonce': nonce,
                   'oauth_signature_method': 'HMAC-SHA1',
                   'oauth_timestamp': unix_time,
                   'oauth_token': oauth.oauth_token,
                   'oauth_version': '1.0'})
    #Signatureの作成
    param_sub.update(oauth_param)
    sign = signature.make_signature(url,
                                   method,
                                   oauth.consumer_secret,
                                   oauth.oauth_token_secret,
                                   param_sub)
    #url_param = {}
    #url_param.update(param)
    #url_param.update({'oauth_signature':urllib.quote(sign, "")})

    #oauth_url = url + "?" + '&'.join(map(concat_param, sorted(url_param.items())))
    #url_param = urllib.urlencode(param)
    #if url_param != '':
    #    oauth_url = "%s?%s" % (url, urllib.urlencode(param))
    #else:
    #    oauth_url = url
    
    url_param = urllib.urlencode(param)
    oauth_url = "%s?%s" % (url, url_param) if url_param else url
    #oauth_url = url
    req = urllib2.Request(oauth_url)

    # Requestにヘッダを付ける
    header_dict = {}
    header_dict.update(oauth_param)
    #header_dict.update(param_sub)
    header_dict.update({'oauth_signature': urllib.quote(sign, "")})
    req.add_header('Authorization', oauth_header(header_dict))


    # Requestにデータをつける
    if data:
        data_str = urllib.urlencode(data)
        req.add_data(data_str)
        req.add_header('Content-Type', content_type)
        req.add_header('Content-Length', str(len(data_str)))
    return req
