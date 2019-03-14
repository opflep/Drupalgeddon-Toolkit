import requests
import re
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
start = time.clock()  
print(start)
with open("last.txt", "r") as ins:
    array = []
    i=1
    for line in ins:
        print(i)
        i=i+1
        host="http://"+line.strip()
        try:
            r = requests.post(host+"/CHANGELOG.txt", verify=False, timeout=2)
            data = r.text
        except Exception as e:
            print("connect error")
            data = ""
        if "Drupal" in data and "<!doctype html>" not in data and "<!DOCTYPE html>" not in data:
            check = True
            sline=0
            while check:
                try:
                    data = r.text.split('\n')[sline]
                except Exception as e:
                    print("no content")
                    check=False
                if "Drupal" in data and "xxxx" not in data and "content=" not in data:
                    check=False
                else:
                    sline=sline+1
            result = host+" "+data
            with open('output/last.txt', 'a') as f:
                f.write("%s\n" % result.encode("utf-8"))
print(time.clock() - start)