# Drupalgeddon-Toolkit

Toolkits that crawl data, drupal sites with version, detect CVE-2018-7600 & CVE-2019-6340 

## Requirements

* Python 2.7 or Python 3.4+
* Works on Linux, Windows

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Crawl data

Crawl websites

```

```

### Check header

From an input file, check header and return site with version of Drupal
$ python Check_Header.py [inputFile] [outputFile]

```
$ python Check_Header.py \input\input_1.txt output_1.txt
```

### Check header

From an input file return site with version of Drupal and update version date by checking CHANGELOG.txt content
$ python Check_CHANGELOG.py [inputFile] [outputFile]

```
$ python Check_CHANGELOG.py \input\input_1.txt output_1.txt
```

## Detect CVE-2018-7600 or CVE-2019-6340

With input file (drupal sites with version) 

```
autocraft-kzn.ru|5
bergerault.com|5
leisureandculturedundee.com|5
...
```

Return normal site and vulnerable site (mark as --|CVE-2018-7600|--) 

```
autocraft-kzn.ru|5
bergerault.com|5 --|CVE-2018-7600|--
leisureandculturedundee.com|5 --|CVE-2018-7600|--
...
...
```

run with command format like: $ python Scan.py [inputFile] [outputFile] [option]
In case want to detect CVE-2018-7600:

```
$ python Scan.py \input\input_1.txt output_1.txt 2018
...
```
OR
```
$ python Scan.py \input\input_1.txt output_1.txt 2019
...
```

## Built With

* [Python2.7](https://docs.python.org/2.7/)
* [Python3.6](https://docs.python.org/2.6/)

## Version

Final version

## Authors

* **VinhPT** - [zeralot](https://github.com/zeralot)
* **VuNX** - [opflep](https://github.com/opflep)

See also the list of [contributors](https://github.com/opflep/Drupalgeddon-Toolkit/graphs/contributors) who participated in this project.
