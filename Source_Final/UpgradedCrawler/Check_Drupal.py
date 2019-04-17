import time
import sys
import requests
import urllib3
import bb01_ultilities as util
from multiprocessing import Pool

start = time.time()
urllib3.disable_warnings()
# Get file input
#file = open(sys.argv[1], 'r')
# Get file output
#outputfile = sys.argv[2]
#lines = file.readlines()
#Get file output
outputfile = sys.argv[1]

def checkHeader(host):
    headers = util.genHeader()
    timeout = 2
    try:
        r = requests.get(host, headers=headers, timeout=timeout)
        if 'Drupal 7' in str(r.headers) and r.status_code == 200:
            return "Drupal 7.xx"
        if 'Drupal 8' in str(r.headers) and r.status_code == 200:
            return "Drupal 8.xx"

    except Exception as e:
        print(e)
        return "N/A"
    return "N/A"


def checkVersion(host):
    headers = util.genHeader()
    timeout = 1
    try:
        # Request to CHANGELOG.txt of host
        r = requests.post(host+"/CHANGELOG.txt",
                          verify=False, headers=headers, timeout=timeout)
        # Case status code != 200
        if(r.status_code != 200):
            # Request to CHANGELOG.txt of host
            r = requests.post(
                host+"/core/CHANGELOG.txt", verify=False, headers=headers, timeout=timeout)
        # Get data
        data = r.text
    except Exception as e:
        return "N/A"
    # Case check drupal
    if "Drupal 1.0.0, 2001-01-15" in data and "<!doctype html>" not in data and "<!DOCTYPE html>" not in data:
        check = True
        sline = 0
        while check:
            try:
                # Get newest version of drupal
                data = r.text.split('\n')[sline]
            except Exception as e:
                check = False
            if "Drupal" in data and "xxxx" not in data and "content=" not in data:
                check = False
            else:
                sline = sline+1
        return data
    else:
        return "N/A"


def checkDrupal(url):
    cleanUrl = url.strip()
    host = "http://"+url.strip()
    result = checkVersion(host)
    if result != "N/A":
        with open(outputfile, 'a') as f:
            f.write("%s|%s\n" % (cleanUrl, result.strip()))
    else:
        result = checkHeader(host)
        if result != "N/A":
            with open(outputfile, 'a') as f:
                f.write("%s|%s\n" % (cleanUrl, result.strip()))
        else:
            with open(outputfile, 'a') as f:
                f.write("%s|%s\n" % (cleanUrl, "N/A"))


if __name__ == "__main__":
    try:
        p = Pool(processes=20)
        result = p.map(checkDrupal, lines)
    except Exception as e:
        with open(outputfile, 'a') as f:
            f.write("|Exception: %s|\n" % e)

    # Open output file and write the total time scanning
    with open(outputfile, 'a') as f:
        f.write("------| Total Time: %s |-------\n" % (time.time() - start))
