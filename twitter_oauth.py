#! /usr/bin/env python
# coding:utf-8


from twitter_parser import JsonParser, SearchInfo, TweetInfo, Status, User, TwitterError 
import oauth

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

class Api:
    def __init__(self, consumer_key, consumer_secret, oauth_token, oauth_token_secret):
        self.api_oauth = oauth.OAuth(consumer_key, consumer_secret, oauth_token, oauth_token_secret)
        self.json_parser = JsonParser()

    def _type_parser(self, content, typ):
        if typ == 'status':
            return self.json_parser.create_status_object(json.loads(content))
        elif typ == 'status_list':
            return self.json_parser.create_status_object_list(json.loads(content))
        elif typ == 'user_list':
            return self.json_parser.create_user_object_list(json.loads(content))
        elif typ == 'user':
            return self.json_parser.create_user_object(json.loads(content))
        elif typ == 'search_info':
            return self.json_parser.create_search_info(json.loads(content))

    def _get_method(self, url, param, typ):
        req = oauth.oauth_request(self.api_oauth, url , 'GET', self._make_param_dict(param))
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

    def _post_method(self, url, param, typ, content_type='application/x-www-form-urlencoded'):
        req = oauth.oauth_request(self.api_oauth, url, 'POST', self._make_param_dict(param), content_type=content_type)
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

    def _str_dict(self, ds):
        '''
        辞書の内容をstrに変換する
        dsにUnicodeがくるとエラーになるので注意
        '''
        rds = {}
        for (key, item) in ds.items():
            rds[key] = str(item)
        return rds

    def _make_param_dict(self, arg_dict):
        url_param_dict = {}
        for (key, item) in arg_dict.iteritems():
            if item:
                url_param_dict.update({key: item})
        return self._str_dict(url_param_dict)

    
    def post_update(self, status, in_reply_to_status_id=None, lat=None, long=None,
                    place_id=None, display_coordinates=None, source=None):
        '''
        Post your tweet.
        '''

        encode_status = status.encode('utf-8')
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

    #def post_update_with_media(self, status, media_url, in_reply_to_status_id=None, lat=None, long=None,
    #                            place_id=None, display_coordinates=None, source=None):
    #
    #    encode_status = status.encode('utf-8')
    #    media_url = media_url.encode('utf-8')
    #    arg_dict = {'status': encode_status,
    #                'media[]': [media_url],
    #                'in_reply_to_status_id':in_reply_to_status_id,
    #                'long':long,
    #                'place_id':place_id,
    #                'display_coordinates':display_coordinates,
    #                'source':source}
    # 
    #    return self._post_method(_UPDATE_WITH_MEDIA_URL, arg_dict, 'status', content_type='form-data')

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
