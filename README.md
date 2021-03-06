# Drupalgeddon-Toolkit

Toolkits that crawl data, drupal sites with version, detect CVE-2018-7600 & CVE-2019-6340 

## Requirements

* Python 2.7 or Python 3.4+
* Works on Linux, Windows

## Getting Started



### Crawl data

Crawl websites


```
Broad Crawl Spider using Scrapy Framework (https://github.com/scrapy/scrapy/tree/master/scrapy)
Warning: Desperately take time, Do not try it at home.
Contact for the sites set
```

---
### Crawler implemented with Check Version
```
From an input file, check header and return site with version of Drupal
> $ python crawl.py [outputFile]

```

---
### Check header

From an input file, check header and return site with version of Drupal
> $ python Check_Header.py [inputFile] [outputFile]

```
$ python Check_Header.py \input\input_1.txt output_1.txt
```

---

### Check CHANGELOG.txt

From an input file return site with version of Drupal and update version date by checking CHANGELOG.txt content
> $ python Check_CHANGELOG.py [inputFile] [outputFile]

```
$ python Check_CHANGELOG.py \input\input_1.txt output_1.txt
```

---

## Detect CVE-2018-7600 or CVE-2019-6340

With input file (drupal sites with version) 

```
...
autocraft-kzn.ru|5
bergerault.com|5
leisureandculturedundee.com|5
...
```

Return normal site and vulnerable site (mark as |VULNERABLE|...) or other cases

```
...
viadux.com.au|8.xx|Redirected|
haapajarvi.fi|8.xx|cleanURL_enable|
esd.ornl.gov|8.xx|N/A|
factsonhand.com|8.3.1|VULNERABLE|
...
```

run with command format like: 
> $ python Scan.py [inputFile] [outputFile] [option]

In case want to detect CVE-2018-7600:

```
$ python Scan.py \input\input_1.txt output_1.txt 2018
...
```
OR CVE-2019-6340
```
$ python Scan.py \input\input_1.txt output_1.txt 2019
...
```
Droopescan
```
$ droopescan scan --check [inputfile_path] --outfile [outputfile_path] --option [option]
...
```

---

## Built With

* [Python2.7](https://docs.python.org/2.7/)
* [Python3.6](https://docs.python.org/2.6/)

## Version

> Draft 
* include all pervious version that incomplete or unresolve bugs 

> Source_Final 
* release version

## Authors
### BB01 team

* **VinhPT** - [zeralot](https://github.com/zeralot)
* **VuNX** - [opflep](https://github.com/opflep)
* **DuyBK** - [chalizard97](https://github.com/chalizard97)
* **TungPT** - [Inf3rnalDr4ke](https://github.com/Inf3rnalDr4ke)
* **HuyTQ** - [1zezus1](https://github.com/1zezus1)

See also the list of [contributors](https://github.com/opflep/Drupalgeddon-Toolkit/graphs/contributors) who participated in this project.
