[![Build Status](https://travis-ci.org/sujitmandal/scrape-search-engine.svg?branch=master)](https://travis-ci.org/sujitmandal/scrape-search-engine) [![GitHub license](https://img.shields.io/github/license/sujitmandal/scrape-search-engine)](https://github.com/sujitmandal/scrape-search-engine/blob/master/LICENSE) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/scrape-search-engine) ![PyPI - Wheel](https://img.shields.io/pypi/wheel/scrape-search-engine) ![PyPI](https://img.shields.io/pypi/v/scrape-search-engine)


[![Downloads](https://pepy.tech/badge/scrape-search-engine)](https://pepy.tech/project/scrape-search-engine)

## Package Installation : 
```
pip install scrape-search-engine
```
[Package LInk](https://pypi.org/project/scrape-search-engine/)

## Scrape Search Engine :

Search anything on the different Search Engine's it will collect all the links and save it into 'json' file format.

## How to import the module:
```
userAgent = ('') #search on google "my user agent"
search = ('')  #Enter Anything for Search
```
## Google Search Engine : 
```
from ScrapeSearchEngine.ScrapeSearchEngine import Google

google = Google(search, userAgent)

print(google)
```
## Duckduckgo Search Engine : 
```
from ScrapeSearchEngine.ScrapeSearchEngine import Duckduckgo

duckduckgo = Duckduckgo(search, userAgent)

print(duckduckgo)
```
## Givewater Search Engine : 
```
from ScrapeSearchEngine.ScrapeSearchEngine import Givewater

givewater = Givewater(search, userAgent)

print(givewater)
```
## Ecosia Search Engine : 
```
from ScrapeSearchEngine.ScrapeSearchEngine import Ecosia

ecosia = Ecosia(search, userAgent)

print(ecosia)
```
## Bing Search Engine : 
```
from ScrapeSearchEngine.ScrapeSearchEngine import Bing

bing = Bing(search, userAgent)

print(bing)
```
## Yahoo Search Engine : 
```
from ScrapeSearchEngine.ScrapeSearchEngine import Yahoo

yahoo = Yahoo(search, userAgent)

print(yahoo)
```
## CommonLinks Search Engine : 
```
from ScrapeSearchEngine.ScrapeSearchEngine import CommonLinks

comminlinks = CommonLinks(search, userAgent)

print(comminlinks)
```
## Save into Json File formate :
```
from ScrapeSearchEngine.ScrapeSearchEngine import makeJson

googleJson = makeJson('google', google)

print(googleJson)

duckduckgoJson = makeJson('duckduckgo', duckduckgo)

print(duckduckgoJson)

givewaterJson = makeJson('givewater', givewater)

print(givewaterJson)

ecosiaJson = makeJson('ecosia', ecosia)

print(ecosiaJson)

bingJson = makeJson('bing', bing)

print(bingJson)
```
## Save All into Json File formate as finalJson :
```
finalJson = makeJson('finalJson',googleJson)

finalJson.update(duckduckgo)

finalJson.update(givewaterJson)

finalJson.update(ecosiaJson)

finalJson.update(bingJson)

print(finalJson)
```

## Required package’s:
```
• pip install BeautifulSoup

• pip install requests

• pip install bs4
```
## License:
MIT Licensed

## Author:
Sujit Mandal

[GitHub](https://github.com/sujitmandal)

[PyPi](https://pypi.org/user/sujitmandal/)

[LinkedIn](https://www.linkedin.com/in/sujit-mandal-91215013a/)