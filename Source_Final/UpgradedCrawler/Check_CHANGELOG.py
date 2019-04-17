import time
import sys
import requests
import urllib3
import bb01_ultilities as util
from random import randint
from multiprocessing import Pool


# Start timer
start = time.time()
urllib3.disable_warnings()
# Get file input
file = open(sys.argv[1], 'r')
# Get file output
outputfile = sys.argv[2]
lines = file.readlines()


def checkVersion(url):
    # Get host as each line of input file
    host = "http://"+url.strip()
    # Get random user agent and set to header
    headers = util.genHeader()
    try:
        # Request to CHANGELOG.txt of host
        r = requests.post(host+"/CHANGELOG.txt",
                          verify=False, headers=headers, timeout=1)
        # Case status code != 200
        if(r.status_code != 200):
            # Request to CHANGELOG.txt of host
            r = requests.post(
                host+"/core/CHANGELOG.txt", verify=False, headers=headers, timeout=1)
        # Get data
        data = r.text
    except Exception as e:
        data = ""
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
        # Concate to result
        result = host+" "+data
        # Open output file
        with open(outputfile, 'a') as f:
            # Write the result to file
            f.write("%s\n" % result.encode("utf-8"))


if __name__ == "__main__":
    try:
        p = Pool(processes=20)
        result = p.map(checkVersion, lines)
    except Exception as e:
        print (e)
    # Open output file and write the total time scanning
    with open(outputfile, 'a') as f:
        f.write("------| Total Time: %s |-------\n" % (time.time() - start))
