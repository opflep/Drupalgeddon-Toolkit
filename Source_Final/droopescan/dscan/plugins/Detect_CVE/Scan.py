from dscan.plugins.Detect_CVE import ultilities as ulti
import requests
import re
import string
import random
import sys
import time
import urllib3
from dscan.plugins.Detect_CVE.Scan_7600 import check_CVE_7600
from dscan.plugins.Detect_CVE.Scan_2019 import isVuln
from functools import partial
from random import randint
from multiprocessing import Pool
import optparse
# Start timer
start = time.time()
urllib3.disable_warnings()

option = 0
def isVulnerable(lines):
    host = "http://"+lines.strip().split("|")[0]+"/"
    version = lines.strip().split("|")[1]
    if (option == "2018"):
        # check CVE 2018-7600
        check, status = check_CVE_7600(host, version)
        if (check is True):
            with open(outputfile, 'a') as f:
                f.write("%s|VULNERABLE|\n" % lines.strip())
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
                f.write("%s|VULNERABLE|\n" % lines.strip())
        elif(status == "NODE"):
            with open(outputfile, 'a') as f:
                f.write("%s|NODE_AVAILABLE|\n" % lines.strip())
        else:
            with open(outputfile, 'a') as f:
                f.write("%s|N/A|\n" % lines.strip())


def main():
    # Get file input
    #file = open(sys.argv[1], 'r')
    # Get file output
    #outputfile = sys.argv[2]
    # Get option CVE detect
    #option = sys.argv[3]
    parse = optparse.OptionParser()
    parse.add_option('--check', default="input.txt", help = "give input file")
    parse.add_option('--outfile', default="output.txt", help = "give output file")
	parse.add_option('--option', default="", help = "give output file")
    opt, args = parse.parse_args()
	option = opt.option
    try: file = open(opt.check, 'r+')
    except Exception as e:
        file = open("input.txt", 'w+')
        file.close()
        file = open("input.txt", "r")
    lines = file.readlines()
    outputfile = ''
    try: outputfile = opt.outfile
    except:
        outputfile = 'output.txt'
    try:
        p = Pool(processes=20)
        result = p.map(isVulnerable, lines)

    except Exception as e:
        with open(outputfile, 'a') as f:
            f.write("Exception - %s\n" % e)

    # Open output file and write the total time scanning
    with open(outputfile, 'a') as f:
        f.write("------| Total Time: %s |-------\n" % (time.time() - start))
