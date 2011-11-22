#! /usr/bin/env python
# coding:utf-8

# signature の作成に必要
import urllib, urllib2
import hmac, hashlib
import time, random
import numbers, mimetypes

def _make_signature_base_string(url, method, parameter):
    '''
        url :: Unicode
        method :: Unicode
        parameter :: dictionary
    '''
    str1 = method + '&' + urllib.quote(url, "") 
    str2 = '&'.join(map(lambda t: t[0] + '=' + t[1], sorted(parameter.items())))
    str2_sub = urllib.quote(str2, "")
    str3 = str1 + '&' + str2_sub
    return str3

def _make_signature(url, method, consumer_secret, access_token_secret, parameter):
    # make key
    key = '%s&%s' % (urllib.quote(consumer_secret, ""), urllib.quote(access_token_secret, ""))
    h = hmac.new(key,
                 _make_signature_base_string(url, method, parameter), 
                 hashlib.sha1)
    sig = h.digest().encode("base64").strip()
    return sig

class OAuth:
    def __init__(self, consumer_key, consumer_secret, oauth_token, oauth_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret

def _parameter_urlencode(param):
    '''
    param :: dictionary
    辞書の要素をURLエンコードーする
    '''
    #return dict(map(lambda pair: map(lambda x:urllib.quote(x, ""), pair), param.items()))
    return dict([(key, urllib.quote(value, "")) for (key, value) in param.iteritems()])

def _concat_header(pair):
    return '%s="%s"' % (pair[0], pair[1])

def _oauth_header(param):
    '''
    param :: dictionary
    '''
    return 'OAuth %s' % ', '.join(map(_concat_header, sorted(param.items())))

def _get_oauth_header(oauth, url, method, params):
    # 乱数の生成
    nonce = str(random.getrandbits(64))
    # システム時間の取得
    unix_time = str(int(time.time()))
    # params のデータをエンコードする
    param_sub = params
    # パラメータ(エンコードしたもの)
    oauth_param = _parameter_urlencode(
                  {'oauth_consumer_key': oauth.consumer_key,
                   'oauth_nonce': nonce,
                   'oauth_signature_method': 'HMAC-SHA1',
                   'oauth_timestamp': unix_time,
                   'oauth_token': oauth.oauth_token,
                   'oauth_version': '1.0'})
    # Signatureの作成
    param_sub.update(oauth_param)
    sign = _make_signature(url,
                           method,
                           oauth.consumer_secret,
                           oauth.oauth_token_secret,
                           param_sub)
    # Requestにヘッダを付ける
    header_dict = {}
    header_dict.update(oauth_param)
    header_dict.update({'oauth_signature': urllib.quote(sign, "")})
    return _oauth_header(header_dict) # Authorization header の追加

# OAuthリクエストの作成
def oauth_request(oauth, url, method, params={}, authentification=False, content_type='application/x-www-form-urlencoded'):
    '''

    '''
    # multipart が有効かどうかのフラグ
    multipart = False
    # params の要素をencode する
    new_params = {}
    for (key, value) in params.iteritems():
        if value==None:
            pass
        elif isinstance(value, numbers.Number):
            new_params[key] = str(value)
        elif isinstance(value, str):
            new_params[key] = urllib.quote(value, '~')
        elif isinstance(value, unicode):
            new_params[key] = urllib.quote(value.encode('utf-8'), '~')
        elif isinstance(value, tuple):
            # この場合はmultipart を有効にする
            new_params[key] = value
            multipart = True
    # url をstr に変更する
    try:
        url = url.encode('utf-8')
    except:
        pass
    # GET method の時
    if method == 'GET':
        # クエリの作成
        paramlist = [key + '=' + value for (key, value) in new_params.iteritems()]
        req = urllib2.Request(url + "?" + "&".join(paramlist))
    # POST method の時
    elif method == 'POST':
        req = urllib2.Request(url)
        # multipart の時
        if multipart:
            boundary = "---PostUpdateWithMediaBoundary"
            datalist = []
            for (key, value) in new_params.iteritems():
                datalist.append('--%s' % boundary)
                if isinstance(value, tuple):
                    filetype = mimetypes.guess_type(value[0])[0]
                    #
                    # filetype がNone の時ののエラーをだす部分を書く
                    #
                    datalist.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (str(key), str(value[0])))
                    datalist.append('Content-Type: %s' % filetype)
                    #datalist.append('Content-Transfer-Encoding: binary')
                    datalist.append('')
                    datalist.append(value[1])
                else:
                    datalist.append('Content-Disposition: form-data; name="%s"' % str(key))
                    datalist.append('')
                    # unquote が必要
                    datalist.append(urllib.unquote(value))
            datalist.append('--%s--' % boundary)
            multipart_data = '\r\n'.join(datalist) + '\r\n'
            req.add_data(multipart_data)
            req.add_header('Content-Type', "%s; boundary=%s" % (content_type, boundary))
            req.add_header('Content-Length', str(len(multipart_data)))
        else:
            # データの作成
            data = [key + '=' + value for (key, value) in new_params.iteritems()]
            # ヘッダにデータを追加する
            req.add_data('&'.join(data))
            # content-type ヘッダーを作成する
            req.add_header('Content-Type', content_type) # Content-type header の追加
            req.add_header('Content-Length', str(len('&'.join(data))))
    else:
        #
        # ここに例外処理を入れること
        #
        pass
    # ヘッダを作成する
    if authentification:
        # authentification するときの処理
        # multipart が有効のとき
        if multipart:
            pa = {}
            #for (key, value) in pa.iteritems():
            #    if isinstance(value, tuple):
            #        pass
            #    else:
            #        pa[key] = value
            #header = _get_oauth_header(oauth, url, method, pa)
            header = _get_oauth_header(oauth, url, method, {})
        # multipart が無効のとき
        else:
            header = _get_oauth_header(oauth, url, method, new_params)
        # header を追加する
        req.add_header('Authorization', header)
    return req
