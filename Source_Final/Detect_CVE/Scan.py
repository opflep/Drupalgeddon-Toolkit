import bb01_ultilities as ulti
import requests
import re
import string
import random
import sys
import time
import urllib3
from Scan_7600 import check_CVE_7600
from Scan_2019 import isVuln
from functools import partial
from random import randint
from multiprocessing import Pool

# Start timer
start = time.time()
urllib3.disable_warnings()
# Get file input
file = open(sys.argv[1], 'r')
# Get file output
outputfile = sys.argv[2]
# Get option CVE detect
option = sys.argv[3]
lines = file.readlines()


def isVulnerable(lines):
    host = "http://"+lines.strip().split("|")[0]+"/"
    version = lines.strip().split("|")[1]
    if (option == "2018"):
        # check CVE 2018-7600
        check, status = check_CVE_7600(host, version)
        if (check is True):
            with open(outputfile, 'a') as f:
                f.write("%s|EXPLOITED|\n" % lines.strip())
        elif(status != ""):
            with open(outputfile, 'a') as f:
                f.write("%s|%s|\n" % (lines.strip(), status))
        else:
            with open(outputfile, 'a') as f:
                f.write("%s|N/A|\n" % lines.strip())
                    
    elif (option == "2019"):
        # Check CVE 2019-6340
        check, status = isVuln(host)
        if (check is True):
            with open(outputfile, 'a') as f:
                f.write("%s|EXPLOITED|\n" % lines.strip())
        elif(status == "NODE"):
            with open(outputfile, 'a') as f:
                f.write("%s|NODE_AVAILABLE|\n" % lines.strip())
        else:
            with open(outputfile, 'a') as f:
                f.write("%s|N/A|\n" % lines.strip())


if __name__ == "__main__":
    try:
        p = Pool(processes=20)
        result = p.map(isVulnerable, lines)

    except Exception as e:
        with open(outputfile, 'a') as f:
            f.write("Exception - %s\n" % e)

    # Open output file and write the total time scanning
    with open(outputfile, 'a') as f:
        f.write("------| Total Time: %s |-------\n" % (time.time() - start))
