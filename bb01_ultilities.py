import random
import requests
import string
import urllib
from urlparse import urljoin

def genSignature(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def isURLValid(url):
	try:
		r = requests.get(url)
	except:
		return False

	return (r.status_code == 200)

def isURLCached(url):
	try:
		r = requests.get(url)
	except:
		return False

	return 'X-Drupal-Cache' in r.headers and r.headers['X-Drupal-Cache'] == 'HIT' and r.status_code == 200


def joinURL(*args):
	url = ''
	for arg in args:
		url = urljoin(url,arg)

	return url