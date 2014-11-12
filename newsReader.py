# Read News Articles' Main text
# Will create a word cloud of it later

# Author: Kuber Chaurasiya 
# Project URL: https://github.com/kuberiitb/randomApps

import urllib2
from BeautifulSoup import *
from urlparse import urljoin

outlook='http://www.outlookindia.com/news/article/Enormous-Passion-for-Knowledge-Reading-in-India-Dan-Brown/867562'
hindu='http://www.thehindu.com/news/national/five-maharashtra-cong-mlas-suspended/article6591234.ece'
hindu2='http://www.thehindu.com/business/govt-lpg-subsidy-capped-at-rs-20-a-kg/article6588020.ece'
hindustanTimes='http://www.hindustantimes.com/india-news/mumbai/maharashtra-5-congress-mlas-suspended-for-injuring-governor/article1-1285404.aspx'
hindustanTimes2='http://www.hindustantimes.com/india-news/why-fadnavis-will-find-it-tough-to-run-maharashtra-with-sena-in-oppn/article1-1285263.aspx'
firstPost='http://www.firstpost.com/politics/maharashtra-live-5-cong-mlas-suspended-after-causing-injury-to-governor-1798883.html'
et='http://economictimes.indiatimes.com/news/politics-and-nation/5-congress-mlas-suspended-for-injuring-governor-c-vidyasagar-rao/articleshow/45125178.cms'
et2='http://economictimes.indiatimes.com/news/company/corporate-trends/surat-diamond-firm-gifts-491-cars-200-two-bedroom-houses-jewellery-to-1200-staff/articleshow/44886868.cms'
et3='http://economictimes.indiatimes.com/news/politics-and-nation/shiromani-akali-dal-and-bjp-race-to-win-dalit-votes-via-bsp-leaders/articleshow/45117406.cms'

url=hindu2
c=urllib2.urlopen(url)
soup=BeautifulSoup(c.read( ))

if 'outlookindia'in url:
    mainText= soup.find('div',{'class': 'finalstorytext3'})
elif 'thehindu.com'in url:
    mainText= soup.find('div',{'class': 'article-text'})
elif 'hindustantimes.com' in url:
    mainText= soup.find('div',{'class': 'sty_txt'})
elif 'firstpost.com' in url:
    mainText= soup.find('div',{'class': 'fullCont'})
elif 'economictimes' in url:
    mainText= soup.find('div',{'class': 'artText'})    
    
# Removing &quotes; and other escapes
import HTMLParser
h = HTMLParser.HTMLParser()
print h.unescape(mainText.text)
# print mainText.text
