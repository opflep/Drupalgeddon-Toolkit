import random
import requests
import string
import urllib
import random
import urllib3
import sys
import time
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


def isURLCached(url):
    headers = util.genHeader()
    timeout = 5
    host = "http://"+url.strip()
    try:
        r = requests.get(host, headers=headers, timeout=timeout)
        if 'Drupal 7' in str(r.headers) and r.status_code == 200:
            with open(outputfile, 'a') as f:
                f.write("%s Drupal 7\n" % url.strip())
        if 'Drupal 8' in str(r.headers) and r.status_code == 200:
            with open(outputfile, 'a') as f:
                f.write("%s Drupal 8\n" % url.strip())
    except Exception as e:
        print (e)


if __name__ == "__main__":
    try:
        p = Pool(processes=20)
        result = p.map(isURLCached, lines)
    except Exception as e:
        print (e)
        # Open output file and write the total time scanning
    with open(outputfile, 'a') as f:
        f.write("------| Total Time: %s |-------\n" % (time.time() - start))
