import requests
import re
import time
import urllib3
import sys
import getopt
import ntpath
from random import randint


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


def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "i:", ["ifile="])
    except getopt.GetoptError:
        print('checkFinal.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('checkFinal.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
    outputfile = "output\output_"+ntpath.basename(inputfile)
    print('-' * 50)
    print('|| Input file is      :', inputfile)
    print('|| Output file is     :', outputfile)
    print('-' * 50)

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    start = time.clock()
    print('Scanning' + ' .' * 15)
    with open(inputfile, "r") as ins:
        array = []
        for line in ins:
            host = "http://"+line.strip()
            headers = {
                'User-Agent': getRandomUserAgent()
            }
            try:
                r = requests.post(host+"/CHANGELOG.txt",
                                  verify=False, headers=headers, timeout=1)
                if(r.status_code != 200):
                    r = requests.post(
                        host+"/core/CHANGELOG.txt", verify=False, headers=headers, timeout=1)
                data = r.text
            except Exception as e:
                data = ""
            if "Drupal 1.0.0, 2001-01-15" in data and "<!doctype html>" not in data and "<!DOCTYPE html>" not in data:
                check = True
                sline = 0
                while check:
                    try:
                        data = r.text.split('\n')[sline]
                    except Exception as e:
                        # print("no content")
                        check = False
                    if "Drupal" in data and "xxxx" not in data and "content=" not in data:
                        check = False
                    else:
                        sline = sline+1
                result = host+" "+data
                with open(outputfile, 'a') as f:
                    f.write("%s\n" % result.encode("utf-8"))
    with open(outputfile, 'a') as f:
        f.write("------| Total Time: %s |-------\n" % (time.clock() - start))


if __name__ == "__main__":
    main(sys.argv[1:])
