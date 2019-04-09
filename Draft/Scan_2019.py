import bb01_ultilities as ulti
import requests
import sys

# Fuction: Find node avaiable for host
# - RETURN:
#     False: No node found
#     node -> string: a node number that available
def findNode(host, min = 1, max = 100 ):
    for node in range (min , max):
        print 'Checking node :' , node
        url = ulti.joinURL(host,'/node/',str(node))
        if ulti.isURLCached(url):
            continue
        if ulti.isURLValid(url):
            print '='*5 + 'Node %s is valid' %node + "="*5 
            return node
    return False


# Fuction: Check if node is vulnerable
# - RETURN:
#     False: Not vul
#     True: Vul
def checkNode(host,node):
    payload = {
        "_links": {
            "type": {
                "href": "%s" % ulti.joinURL(host, '/rest/type/node/BB01_Trig')
            }
        },
        "type": {
            "target_id": "article"
        },
        "title": {
            "value": "My Article"
        },
        "body": {
            "value": ""
        }
    }

    url = ulti.joinURL(host,'/node/',str(node))
    r = requests.get('%s?_format=hal_json' %url, json=payload, headers={"Content-Type": "application/hal+json"})
    
    if ulti.isURLCached(r):
        return 'May wrong'
    if 'BB01_Trig does not correspond to an entity on this site' in r.text:
        return True
    
    return False


# Fuction: Check if host is vuln
# - RETURN:
#     False: No vuln
#     True: Vul
def isVuln(host):
    try:
        node = findNode(host)
        if(node):
            return checkNode(host, node)
        else:
            return False
    except:
        return False

if __name__ == '__main__':
    host = 'http://68.183.237.96'
    print host
    if(isVuln(host)):
        print 'Host is vulnerable'