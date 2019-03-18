import requests
import re
import time
import urllib3
import sys
import getopt
import ntpath


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
            try:
                r = requests.post(host+"/CHANGELOG.txt",
                                  verify=False, timeout=2)
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
