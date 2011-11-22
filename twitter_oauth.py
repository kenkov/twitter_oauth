#! /usr/bin/env python
# coding:utf-8

from twitter_parser import JsonParser, SearchInfo, TweetInfo, Status, User
import oauth
import traceback
import urllib, urllib2
#import simplejson as json
import json

_UPDATE_URL = 'http://api.twitter.com/1/statuses/update.json'
_RETWEET_URL = 'http://api.twitter.com/1/statuses/retweet/%s.json'
_UPDATE_WITH_MEDIA_URL = 'https://upload.twitter.com/1/statuses/update_with_media.json'
_FRIENDS_TIMELINE_URL = 'http://api.twitter.com/1/statuses/home_timeline.json'
_USER_TIMELINE_URL = 'http://api.twitter.com/1/statuses/user_timeline.json'
_REPLIES_URL = 'http://api.twitter.com/1/statuses/replies.json'
_SHOW_STATUS_URL = 'http://api.twitter.com/1/statuses/show/%s.json'
_DESTROY_URL = 'http://api.twitter.com/1/statuses/destroy/%s.json'
_LIST_STATUS_URL = 'http://api.twitter.com/1/%s/lists/%s/statuses.json'
_CREATE_FRIENDSHIP_URL = 'http://api.twitter.com/1/friendships/create/%s.json'
_DESTROY_FRIENDSHIP_URL = 'http://api.twitter.com/1/friendships/destroy/%s.json'
_SEARCH_USER_URL = 'http://api.twitter.com/1/users/search.json'
_SHOW_USER_URL = 'http://api.twitter.com/1/users/show/%s.json'
_SEARCH_URL = 'http://search.twitter.com/search.json'

_CREATE_FAVORITE_URL = 'http://api.twitter.com/1/favorites/create/%s.json'
_DESTROY_FAVORITE_URL = 'http://api.twitter.com/1/favorites/destroy/%s.json'
_SHOW_FAVORITE_URL = 'http://api.twitter.com/1/favorites/%s.json'

_RETWEETED_BY_ME = 'http://api.twitter.com/1/statuses/retweeted_by_me.json' 

# stream API
_USER_STREAM_URL = 'https://userstream.twitter.com/2/user.json'

class Api(object):
    def __init__(self, consumer_key, consumer_secret, oauth_token, oauth_token_secret):
        self._api_oauth = oauth.OAuth(consumer_key, consumer_secret, oauth_token, oauth_token_secret)
        self._json_parser = JsonParser()

    def _get_api_oauth(self):
        return self._api_oauth

    def _get_json_parser(self):
        return self._json_parser

    api_oauth = property(_get_api_oauth)
    json_parser = property(_get_json_parser)

    def _type_parser(self, content, typ):
        if typ == 'status':
            return self._json_parser.create_status_object(json.loads(content))
        elif typ == 'status_list':
            return self._json_parser.create_status_object_list(json.loads(content))
        elif typ == 'user_list':
            return self._json_parser.create_user_object_list(json.loads(content))
        elif typ == 'user':
            return self._json_parser.create_user_object(json.loads(content))
        elif typ == 'search_info':
            return self._json_parser.create_search_info(json.loads(content))

    def _get_method(self, url, param, typ, authentification=True):
        req = oauth.oauth_request(oauth=self._api_oauth,
                                  url=url,
                                  method='GET',
                                  params=param,
                                  authentification=authentification)
        try:
            #print 'DATA: %s' % req.get_data()
            #print 'METHOD: %s' % req.get_method()
            #print 'HOST: %s' % req.get_host()
            #print 'URL: %s' % req.get_full_url()
            #print 'HEADER: %s' % req.get_header('Authorization')
            #print "Error: %s" % e
            res = urllib2.urlopen(req)
            content = res.read()
            return self._type_parser(content, typ)
        except urllib2.HTTPError, e:
            print e.read()

    def _post_method(self, url, param, typ, authentification=True, content_type='application/x-www-form-urlencoded'):
        req = oauth.oauth_request(oauth=self._api_oauth,
                                  url=url,
                                  method='POST',
                                  params=param,
                                  authentification=authentification,
                                  content_type=content_type)
        try:
            #print 'DATA: %s' % req.get_data()
            #print 'METHOD: %s' % req.get_method()
            #print 'HOST: %s' % req.get_host()
            #print 'URL: %s' % req.get_full_url()
            #print 'HEADER: %s' % req.get_header('Authorization')
            res = urllib2.urlopen(req)
            content = res.read()
            return self._type_parser(content, typ)
        except urllib2.HTTPError, e:
            print "Error: %s" % e
            print e.read()

    def post_update(self, status, in_reply_to_status_id=None, lat=None, long=None,
                    place_id=None, display_coordinates=None, source=None):
        '''
        Post your tweet.
        '''
        encode_status = status
        arg_dict = {'status': encode_status,
                    'in_reply_to_status_id':in_reply_to_status_id,
                    'lat':lat,
                    'long':long,
                    'place_id':place_id,
                    'display_coordinates':display_coordinates,
                    'source':source}

        return self._post_method(_UPDATE_URL, arg_dict, 'status')

    def retweet(self, id, include_entities=None, trim_user=None):
        arg_dict = {'id':id , 'include_entities':include_entities, 'trim_user':trim_user}
        print _RETWEET_URL % id
        return self._post_method(_RETWEET_URL % id, arg_dict, 'status')

    def post_update_with_media(self, status, media_url, in_reply_to_status_id=None, lat=None, long=None,
                                place_id=None, display_coordinates=None):
    
        encode_status = status
        media_url = media_url
        media = open(media_url, 'rb').read()
        arg_dict = {'status': encode_status,
                    'media[]': (media_url, media),
                    'in_reply_to_status_id':in_reply_to_status_id,
                    'long':long,
                    'place_id':place_id,
                    'display_coordinates':display_coordinates}
        return self._post_method(_UPDATE_WITH_MEDIA_URL, arg_dict, 'status', content_type='multipart/form-data')

    def get_user_timeline(self, id=None, since_id=None, max_id=None,
                             count=None, page=None):
        
        arg_dict = {'id':id , 'since_id':since_id, 'max_id':max_id,
                    'count':count, 'page':page}
        return self._get_method(_USER_TIMELINE_URL, arg_dict, 'status_list')

    def get_friends_timeline(self, id=None, since_id=None, max_id=None,
                             count=None, page=None):
        
        arg_dict = {'id':id , 'since_id':since_id, 'max_id':max_id,
                    'count':count, 'page':page}
        return self._get_method(_FRIENDS_TIMELINE_URL, arg_dict, 'status_list')

    def get_replies(self, id=None, since_id=None, max_id=None,
                    count=None, page=None):

        # parse args
        arg_dict = {'id':id , 'since_id':since_id, 'max_id':max_id,
                    'count':count, 'page':page}
        return self._get_method(_REPLIES_URL, arg_dict, 'status_list')

    def show_status(self, id):
        '''
        get status which has a id
        '''
        # create url
        url = _SHOW_STATUS_URL % id
        return self._get_method(url, {'id':id}, 'status')

    def destroy_status(self, id):
        
        url = _DESTROY_URL % id
        return self._post_method(url, {'id':id}, 'status')

    def get_list_status(self, user, list_id, since_id=None, max_id=None, per_page=None):
        
        # parse args
        arg_dict = {'list_id':list_id , 'since_id':since_id, 'max_id':max_id,
                    'per_page':per_page}
        url = _LIST_STATUS_URL % (user, list_id)
        return self._get_method(url, arg_dict, 'status_list')


    def create_friendship(self, id, follow=None):
        arg_dict = {'follow':follow, 'id':id}
        url = _CREATE_FRIENDSHIP_URL % id
        return self._post_method(url, arg_dict, 'user')

    def destroy_friendship(self, id):
        arg_dict = {'id':id}
        url = _DESTROY_FRIENDSHIP_URL % id
        return self._post_method(url, arg_dict, 'user')

    def search_user(self, q, per_page=None, page=None):
                            #user_id=None, screen_name=None  
        '''
        q:unicode
        '''
        arg_dict = {'q':q.encode('utf-8'), 'per_page':per_page, 'page':page}
        return self._get_method(_SEARCH_USER_URL, arg_dict, 'user_list')

    def show_user(self, id):
                 #user_id=None, screen_name=None  
        arg_dict = {'id':id}
        url = _SHOW_USER_URL % id
        return self._get_method(url, arg_dict, 'user')

    def search(self, q, callback=None, lang=None, locale=None, 
                rpp=None, page=None, max_id=None, since_id=None,
                since=None, until=None, geocode=None, show_user=None):
        '''
        q:unicode
        '''
        arg_dict = {'q':q.encode('utf-8'), 'callback':callback, 'lang':lang,
                    'locale':locale, 'rpp':rpp, 'page':page, 'max_id':max_id,
                    'since_id':since_id, 'since':since, 'until':until, 
                    'geocode':geocode, 'show_user':show_user}
        return self._get_method(_SEARCH_URL, arg_dict, 'search_info')

    def create_favorite(self, id):
        """
        create favotie
        """
        url = _CREATE_FAVORITE_URL % id
        arg_dict = {'id':id}
        return self._post_method(url, arg_dict, 'status')

    def destroy_favorite(self, id):
        """
        create favotie
        """
        url = _DESTROY_FAVORITE_URL % id
        arg_dict = {'id':id}
        return self._post_method(url, arg_dict, 'status')

    def show_favorite(self, id, page=None):

        url = _SHOW_FAVORITE_URL % id
        arg_dict = {'id':id, 'page':page}
        return self._get_method(url, arg_dict, 'status_list')

    def retweeted_by_me(self, count=None, since_id=None, max_id=None, page=None, trim_user=None, include_entities=None):
        arg_dict = {'since_id':since_id, 'max_id':max_id, 'count':count, 'page':page,
                    'trim_user':trim_user, 'include_entities':include_entities}
        return self._get_method(_RETWEETED_BY_ME, arg_dict, 'status_list')

    def user_stream(self):
        def get_user_stream():
            req = oauth.oauth_request(oauth=self._api_oauth, url=_USER_STREAM_URL, method='GET', params={}, authentification=True)
            return urllib2.urlopen(req, timeout=90.0)
        # コネクションする
        stream = get_user_stream()
        # はじめのfollow 情報はすてる
        while True:
            response = ""
            while True:
                c = stream.read(1)
                if c == '\n':
                    break
                response += c
            break
        # statu を取得する
        while True:
            response = ""
            while True:
                # 1 byte をread する
                c = stream.read(1)
                # 改行だったらbreak する
                if c == '\n':
                    break
                # 改行でなかったらresponse に繋げる
                else:
                    response += c
            # response をstrip する
            strip_res = response.strip()
            # コネクションを確立しておくための
            # white space はすてる
            if strip_res == '':
                #print "WHITE SPACE"
                continue
            try:
                status = self._json_parser.create_status_object(json.loads(strip_res))
                yield status
            except:
                #
                # ここは対処をする
                # dev.twitter.com のドキュメントを読む
                #
                #
                # event, delete, ...
                # などに対処する必要がある．
                #
                #print strip_res
                pass

class TwitterError(Exception):
    '''
    A class representing twitter error.

    A TwitterError is raised when a status code is not 200 returned from Twitter.
    '''
    def __init__(self, status=None, content=None):
        '''
        res : status code
        content : XML
        '''
        Exception.__init__(self)

        self._status = status
        self._content = content

    def _get_response(self):
        ''' Return status code '''
        return self.status

    def _get_content(self):
        ''' Return XML '''
        return self.content

    status = property(_get_response)
    content = property(_get_content)

    def __str__(self):
        return 'status_code:%s' % self.status
