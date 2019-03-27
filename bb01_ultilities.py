import random
import requests
import string
import urllib
import random
import sys
import time
from random import randint
from urlparse import urljoin


def getRandomUserAgent():
    user_agents = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:38.0) Gecko/20100101 Firefox/38.0",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
                   "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
                   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
                   "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36",
                   "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0",
                   "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)",
                   "Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1)",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0",
                   "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
                   "Opera/9.80 (Windows NT 6.2; Win64; x64) Presto/2.12.388 Version/12.17",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0"]
    return user_agents[randint(0, len(user_agents) - 1)]

def genHeader():
	return{
        'User-Agent': getRandomUserAgent()
    }

def genSignature(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

# To-do : abohn.org|7.44
def isURLRedirected(url, timeout = 1):
	headers = genHeader()
	try:
		res = requests.get(url, headers=headers, timeout = timeout)
	except :
		return False
	
	return res.url

def isURLValid(url,headers = genHeader(), timeout = 1):
	headers = genHeader()
	try:
		r = requests.get(url, headers=headers, timeout = timeout)
	except:
		return False

	return (r.status_code == 200)

def isURLCached(url,headers = genHeader(), timeout = 1):
	headers = genHeader()
	try:
		r = requests.get(url, headers=headers, timeout = timeout)
	except:
		return False

	return 'X-Drupal-Cache' in r.headers and r.headers['X-Drupal-Cache'] == 'HIT' and r.status_code == 200


def joinURL(*args):
	url = ''
	for arg in args:
		url = urljoin(url,arg)

	return url