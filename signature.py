#! /usr/bin/env python
# coding:utf-8

import urllib, urllib2
import hmac, hashlib

def make_signature_base_string(url, method, parameter):
    '''
        url :: Unicode
        method :: Unicode
        parameter :: dictionary
    '''
    str1 = method + '&' + urllib.quote(url, "") 
    str2 = '&'.join(map(lambda t: t[0] + '=' + t[1], sorted(parameter.items())))
    str2_sub = urllib.quote(str2, "")
    str3 = str1 + '&' + str2_sub
    #print str3
    return str3

def make_signature(url, method, consumer_secret, access_token_secret, parameter):
    # make key
    key = '%s&%s' % (urllib.quote(consumer_secret, ""), urllib.quote(access_token_secret, ""))
    h = hmac.new(key,
                 make_signature_base_string(url, method, parameter), 
                 hashlib.sha1)
    sig = h.digest().encode("base64").strip()

    # すでにencodeしたものを返すようにしてある
    #return urllib.quote(sig, "")
    return sig
