#! /usr/bin/env python
# coding:utf-8

import datetime

class JsonParser(object):
    def __init__(self):
        pass

    def set_value(self, res, value):
            if res.has_key(value):
                try:
                    return res[value].decode('utf-8')
                except:
                    return res[value]
            else:
                return None

    def create_search_info(self, search_dict):
        '''
        search_dict is a json dictionary got from twitter
        >>> create_search_info(json.loads(json_str))
        '''
        return SearchInfo(self.create_tweet_info(search_dict['results']),
                          self.set_value(search_dict,'max_id'), self.set_value(search_dict,'since_id'),
                          self.set_value(search_dict,'refresh_url'), self.set_value(search_dict, 'next_page'), self.set_value(search_dict,'results_per_page'),
                          self.set_value(search_dict,'page'), self.set_value(search_dict,'completed_in'), self.set_value(search_dict,'query'))

    def create_tweet_info(self, results):
        '''
        results = json.loads(search_json)['results']

        to_userキーを持つ時と持たない時がある...
        '''
        return [TweetInfo(self.set_value(res, 'created_at'),self.set_value(res,'id'),self.set_value(res,'text'),
                          self.set_value(res,'from_user'),self.set_value(res,'from_user_id'),
                          self.set_value(res,'to_user'),self.set_value(res,'to_user_id'),self.set_value(res,'profile_image_url'),
                          self.set_value(res,'geo'), self.set_value(res,'iso_language_code'), self.set_value(res,'source')) for res in results]

    def create_status_object(self,status_dict):
        '''
        >>> create_status_object(json.loads(json_str))
        '''
        status_obj = Status(created_at=self.set_value(status_dict, 'created_at'), 
                            id=self.set_value(status_dict, 'id'), 
                            text=self.set_value(status_dict, 'text'),
                            source=self.set_value(status_dict, 'source'),
                            truncated=self.set_value(status_dict, 'truncated'), 
                            in_reply_to_status_id=self.set_value(status_dict, 'in_reply_to_status_id'),
                            in_reply_to_user_id=self.set_value(status_dict, 'in_reply_to_user_id'),
                            favorited=self.set_value(status_dict, 'favorited'), 
                            user=self.create_user_object(status_dict['user']),
                            geo=self.set_value(status_dict, 'geo'),
                            contributors=self.set_value(status_dict, 'contributors'))

        return status_obj

    def create_user_object(self, user_dict):
        '''
        >>> create_user_object(json.loads(json_str))
        '''
        user_obj = User(id=self.set_value(user_dict, 'id'), name=self.set_value(user_dict, 'name'),
                        screen_name=self.set_value(user_dict, 'screen_name'), 
                        created_at=self.set_value(user_dict, 'created_at'),
                        location=self.set_value(user_dict, 'location'),
                        description=self.set_value(user_dict, 'description'),
                        url=self.set_value(user_dict, 'url'),
                        protected=self.set_value(user_dict, 'protected'), 
                        followers_count=self.set_value(user_dict, 'followers_count'),
                        friends_count=self.set_value(user_dict, 'friends_count'), 
                        favourites_count=self.set_value(user_dict, 'favourites_count'),
                        statuses_count=self.set_value(user_dict, 'statuses_count'),
                        profile_image_url=self.set_value(user_dict, 'profile_image_url'),
                        profile_background_color=self.set_value(user_dict, 'profile_background_color'),
                        profile_text_color=self.set_value(user_dict, 'profile_text_color'),
                        profile_link_color=self.set_value(user_dict, 'profile_link_color'),
                        profile_sidebar_fill_color=self.set_value(user_dict, 'profile_sidebar_fill_color'),
                        profile_sidebar_border_color=self.set_value(user_dict, 'profile_sidebar_border_color'),
                        profile_background_image_url=self.set_value(user_dict, 'profile_background_image_url'),
                        profile_background_tile=self.set_value(user_dict, 'profile_background_tile'),
                        utc_offset=self.set_value(user_dict, 'utc_offset'),
                        time_zone=self.set_value(user_dict, 'time_zone'),
                        lang=self.set_value(user_dict, 'lang'),
                        geo_enabled=self.set_value(user_dict, 'geo_enabled'),
                        verified=self.set_value(user_dict, 'verified'),
                        notifications=self.set_value(user_dict, 'notifications'),
                        following=self.set_value(user_dict, 'following'), 
                        contributors_enabled=self.set_value(user_dict, 'contributors_enabled'))

        return user_obj

    def create_status_object_list(self, status_list):
        """ return genexp """
        return (self.create_status_object(i) for i in status_list)


    def create_user_object_list(self, user_list):
        '''
        Create a User object list from xml.getElementsByTagName('user')
        return genexp
        '''
        return (self.create_user_object(i) for i in user_list)

class SearchInfo(object):
    def __init__(self, results, max_id, since_id,
                 refresh_url, next_page, results_per_page,
                 page, completed_in, query):

        self.results = results
        self.max_id = max_id
        self.since_id = since_id
        self.refresh_url = refresh_url
        self.next_page = next_page
        self.results_per_page = results_per_page
        self.page = page
        self.completed_in = completed_in
        self.query = query

class TweetInfo(object):
    def __init__(self, created_at, id, text,
                 from_user, from_user_id, to_user,
                 to_user_id, profile_image_url, geo,
                 iso_language_code, source):
        
        self.created_at = created_at
        self.id = id
        self.text = text
        self.from_user = from_user
        self.from_user_id = from_user_id
        self.to_user = to_user
        self.to_user_id = to_user_id
        self.profile_image_url = profile_image_url
        self.geo = geo
        self.iso_language_code = iso_language_code
        self.source = source

    def _create_datetime_obj(self, utc_datetime):
        '''
        Create datetime object
        Thu, 14 Oct 2010 08:35:44 +0000 <type 'str'>
        input : utc_datetime = u'Sun Jul 25 14:12:06 +0000 2010'
        return : str(datetime.datetime(2010,07,26,23,12)
        '''
        month_str = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 
                     'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}

        sub = utc_datetime.split()
        utc_datetime_list = [sub[0][:-1], sub[2], sub[1], sub[4], sub[5], sub[3]]
        utc_time = utc_datetime_list[3].split(':')

        utc_now = datetime.datetime(int(utc_datetime_list[5]), 
                                    int(month_str[utc_datetime_list[1]]),
                                    int(utc_datetime_list[2]),
                                    int(utc_time[0]),
                                    int(utc_time[1]))

        return utc_now

    def get_created_at_from_now(self):
        '''
        When created from now
        '''

        t = datetime.datetime.utcnow() - self._create_datetime_obj(self.created_at)
        day = t.days
        sec = t.seconds
        min = sec / 60
        hour = min / 60

        if t.days >= 1:
            return u'%s days ago' % str(day)
        elif hour >= 1:
            return u'%s hours ago' % str(hour)
        elif min >= 1:
            return u'%s minutes ago' % (str(min))
        else:
            return u'%s seconds ago' % (str(sec))

    def get_created_at_in_utc(self):
        '''
        return datetime.datetime object in UTC
        '''
        return self._create_datetime_obj(self.created_at)

    def get_created_at_in_jsp(self):
        '''
        return datetime.datetime object in JSP
        '''
        return self._create_datetime_obj(self.created_at) + datetime.timedelta(hours=9)

class Status(object):
    '''
    A class representing a status.

    The Status class have next attributes:

        stauts.created_at
        stauts.id
        stauts.text
        stauts.source
        stauts.truncated
        stauts.in_reply_to_status_id
        stauts.in_reply_to_user_id
        stauts.favorited
        stauts.user
        stauts.geo
        stauts.contributors

    The Status class have next methods:

        status.get_created_at_from_now()
        status.get_created_at_in_utc()
        status.get_created_at_in_jsp()

    '''
    def __init__(self, 
                 created_at=None, id=None, text=None,
                 source=None, truncated=None, in_reply_to_status_id=None,
                 in_reply_to_user_id=None,
                 favorited=None, user=None,
                 geo=None, contributors=None):
        '''
        Status class initializer.
        '''
        self.created_at = created_at
        self.id = id
        self.text = text
        self.source = source
        self.truncated = truncated
        self.in_reply_to_status_id = in_reply_to_status_id
        self.in_reply_to_user_id = in_reply_to_user_id
        self.favorited = favorited
        self.user = user
        self.geo = geo
        self.contributors = contributors

    def _create_datetime_obj(self, utc_datetime):
        '''
        Create datetime object

        input : utc_datetime = u'Sun Jul 25 14:12:06 +0000 2010'
        return : str(datetime.datetime(2010,07,26,23,12)
        '''
        month_str = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 
                     'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
        utc_datetime_list = utc_datetime.split()
        utc_time = utc_datetime_list[3].split(':')

        utc_now = datetime.datetime(int(utc_datetime_list[5]), 
                                    int(month_str[utc_datetime_list[1]]),
                                    int(utc_datetime_list[2]),
                                    int(utc_time[0]),
                                    int(utc_time[1]))
        return utc_now

    def get_created_at_from_now(self):
        '''
        When created from now
        '''
        t = datetime.datetime.utcnow() - self._create_datetime_obj(self.created_at)
        day = t.days
        sec = t.seconds
        min = sec / 60
        hour = min / 60

        if t.days >= 1:
            return u'%s days ago' % str(day)
        elif hour >= 1:
            return u'%s hours ago' % str(hour)
        elif min >= 1:
            return u'%s minutes ago' % (str(min))
        else:
            return u'%s seconds ago' % (str(sec))

    def get_created_at_in_utc(self):
        '''
        return datetime.datetime object in UTC
        '''

        return self._create_datetime_obj(self.created_at)

    def get_created_at_in_jsp(self):
        '''
        return datetime.datetime object in JSP
        '''

        return self._create_datetime_obj(self.created_at) + datetime.timedelta(hours=9)

    def __cmp__(self, other):
        if self.get_created_at_in_jsp() > other.get_created_at_in_jsp():
            return -1
        elif self.get_created_at_in_jsp() == other.get_created_at_in_jsp():
            return 0
        else:
            return 1

class User(object):
    '''
    A class representing User.

    The User class have next attributes:

        user.id
        user.name
        user.screen_name
        user.created_at
        user.location
        user.description
        user.url
        user.protected
        user.followers_count
        user.friends_count
        user.favourites_count
        user.statuses_count
        user.profile_image_url
        user.profile_background_color
        user.profile_text_color
        user.profile_link_color
        user.profile_sidebar_fill_color
        user.profile_sidebar_border_color
        user.profile_background_image_url
        user.profile_background_tile
        user.utc_offset
        user.time_zone
        user.lang
        user.geo_enabled
        user.verified
        user.notifications
        user.following
        user.contributors_enabled

    The Status class have next methods:

        status.get_created_at_in_utc()
        status.get_created_at_in_jsp()

    '''
    def __init__(self, 
                 id=None, name=None, screen_name=None, 
                 created_at=None, location=None, description=None,
                 url=None, protected=None, followers_count=None, friends_count=None, 
                 favourites_count=None, statuses_count=None, profile_image_url=None,
                 profile_background_color=None, profile_text_color=None,
                 profile_link_color=None, profile_sidebar_fill_color=None,
                 profile_sidebar_border_color=None,
                 profile_background_image_url=None,
                 profile_background_tile=None,
                 utc_offset=None, time_zone=None, lang=None, geo_enabled=None,
                 verified=None, notifications=None, following=None, 
                 contributors_enabled=None):

        self.id = id
        self.name = name
        self.screen_name = screen_name
        self.created_at = created_at
        self.location = location
        self.description = description
        self.url = url
        self.protected = protected
        self.followers_count = followers_count
        self.friends_count = friends_count
        self.favourites_count = favourites_count
        self.statuses_count = statuses_count
        self.profile_image_url = profile_image_url
        self.profile_background_color = profile_background_color
        self.profile_text_color = profile_text_color
        self.profile_link_color = profile_link_color
        self.profile_sidebar_fill_color = profile_sidebar_fill_color
        self.profile_sidebar_border_color = profile_sidebar_border_color
        self.profile_background_image_url = profile_background_image_url
        self.profile_background_tile = profile_background_tile
        self.utc_offset = utc_offset
        self.time_zone = time_zone
        self.lang = lang
        self.geo_enabled = geo_enabled
        self.verified = verified
        self.notifications = notifications
        self.following = following
        self.contributors_enabled = contributors_enabled

    def _create_datetime_obj(self, utc_datetime):
        '''
        Create a datetime object.

        input : utc_datetime = u'Sun Jul 25 14:12:06 +0000 2010'
        return : str(datetime.datetime(2010,07,26,23,12)
        '''
        month_str = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 
                     'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
        utc_datetime_list = utc_datetime.split()
        utc_time = utc_datetime_list[3].split(':')

        utc_now = datetime.datetime(int(utc_datetime_list[5]), 
                                    int(month_str[utc_datetime_list[1]]),
                                    int(utc_datetime_list[2]),
                                    int(utc_time[0]),
                                    int(utc_time[1]))
        return utc_now

    def get_created_at_in_utc(self):
        '''
        return datetime.datetime object in UTC
        '''
        return self._create_datetime_obj(self.created_at)

    def get_created_at_in_jsp(self):
        '''
        return datetime.datetime object in JSP
        '''
        return self._create_datetime_obj(self.created_at) + datetime.timedelta(hours=9)
