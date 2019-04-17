import urllib3
import sys
import time
import requests
import Check_Drupal as check
def getHtml(a):
	i = a.find("/", 8)
	return a[0:i+1]
response = requests.get("https://scrapinghub.com")
data = response.text

start = time.time()

filename = "test1" + '.txt'
f = open(filename,'w+')	
webContent = response.text
count = 0
URL_seen = {"https://scrapinghub.com/"}
URL_visited = ["https://scrapinghub.com/"]
for x in URL_visited:
	print(count)
	#print "opening url: " + x
	if x!= "https:":
		try: response = requests.get(x)
		#except urllib2.URLError as e:
		#	print e.reason
		except:
			b = 1
	webContent = response.text
	a = webContent.find("https://")
	while a!= -1:
		i = webContent.find(" ",a+1)
		j = webContent.find("\"",a+1)
		if i<j:
			URL_visited.append(webContent[a:i])
			try: html = getHtml(webContent[a:i])
			except: b = 1
		else:
			URL_visited.append(webContent[a:j])
			try: html = getHtml(webContent[a:j])
			except: b = 1
		if html not in URL_seen:
			#print html
			check.checkDrupal(html)
			URL_seen.add(html)
			f.write(html)
			f.write("\n")
		a = webContent.find("https://",a+1)
	count = count + 1
f.close()
print("done")


