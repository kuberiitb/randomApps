#!/usr/bin/env python
'''
Given name of the movie, this code 
	* downloads the correct subtitle from subscene.com(as of now)
	* unzip it and 
	* rename it to the filename provided

Input format:
	* Please give filename as it is, with extension(eg .mp4, .avi etc). 
	* The output file will be as same name of this input, ignoring the extension 
	  and add actual extension of subtitle while creting it.
	* Add an s at the end if you don't need the details to be printed on the console
Example:
	* python autosubdownloader.py Horrible.Bosses.2.2014.1080p.BluRay.x264.YIFY.mp4
Bug(s):
subscene may not givecorrect subtitle at first rank. Need to select the correct subtitle before/downloading

'''

###############################################################################
''' libraries required
'''
import sys
import os
import time
import shutil
from bs4 import BeautifulSoup
from urlparse import urljoin
import urllib2
import cookielib
import zipfile

###############################################################################
''' Parameters to be used
'''
siteQuery = {
	'subscene':'http://www.subscene.com/subtitles/release?q='
	#,'opensubtitles':'http://www.opensubtitles.org/en/search2/sublanguageid-eng/moviename-'
	}
siteFind = {'subscene': 'lambda tag: tag.name==\'table\''
	#,'opensubtitles':'lambda tag: tag.name==\'table\' and tag.has_attr(\'id\') and tag[\'id\'] == \'search_results\''
	}

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

try:
	fileName = sys.argv[1]
except:
	fileName = 'suits.s05e16.hdtv.x264-killers[ettv].mp4'
try:
	mode = sys.argv[2]
except:
	mode = 'normal'

fileNameCleaned = '.'.join(fileName.split('.')[:-1])

###############################################################################
''' Required Functions	
'''
def printing(text):
	if mode!='silent':
		print text 
	else:
		return 0

def unZipFile(zipName, outFileName=fileNameCleaned):
	''' Extract the given file
	'''
	unzipped = multipleFileFlag = 0
	#printing(zipName)
	try:
		zfile = zipfile.ZipFile(zipName)
		with zipfile.ZipFile(zipName) as zfile:
			for name in zfile.namelist():
				if multipleFileFlag > 0:
					printing("Multiple Files exists in the archive!!!!")
				(dname, fname) = os.path.split(name)
				if fname.find('.sub')>0 or fname.find('.srt')>0  or fname.find('.py')>0:
					zfile.extract(fname, '.')
		unzipped=1
	except BadZipfile:
		printing("could not extract")
		return False


	fname1, ext  = '.'.join(fname.split('.')[:-1]), '.' + fname.split('.')[-1]
	shutil.move(fname, outFileName + ext)
	printing("Actual filename" + fname + ext + ' Renamed to ' + outFileName + ext)
	if unzipped==1:
		return True


def subscene(tableRows):
	''' Download subtitle from subscene.com
	'''
	downloaded = 0
	for tableRow in tableRows:
		if downloaded > 0:
			return 0
		cell = tableRow.find('td', {'class':'a1'})
		#printing(cell)
		if cell is None:
			continue
		#return 0
		lang= str(cell.find('span', {'class':'l r neutral-icon'}).text.strip())
		#printing(lang)
		if lang== 'English':
			link = 'http://www.subscene.com' + cell.find('a').get('href')
			printing("Trying " + link)
			# http://subscene.com/subtitles/suits-fifth-season/english/1288979
			downloadSoup = crawl(link, 'subscene', 1)
			downloadLink = 'http://subscene.com' + downloadSoup.find('div',{'class','download'}).find('a').get('href')
			#put exception here
			with open(fileNameCleaned + '.zip','w') as zipFileName:
				zipToDownload = urllib2.urlopen(urllib2.Request(downloadLink, headers=hdr))
				zipFileName.write(zipToDownload.read())
				downloaded = 1
				printing("Downloaded file")
			unZipFile(fileNameCleaned + '.zip')
 
def crawl(link, site, justSoup=0):
	''' get the list of subtitle from sites and pass it to relevant functions
	'''
	req = urllib2.Request(link, headers=hdr)
	try:
		page = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
   		printing(e.fp.read())
	soup = BeautifulSoup(page.read())
	#printing(soup)
	if justSoup==1:
		return soup
	tableSite = eval('soup.find(' + siteFind[site] + ')' )
	tableRows = tableSite.findChildren(['tr'])#['th', 'tr'])
	if site == 'subscene':
		subscene(tableRows)

if __name__ == '__main__': 
	for q in siteQuery.keys():
		searchUrl = siteQuery[q] + fileNameCleaned
		printing(q + ' ' + searchUrl)
		printing('Querying for  ' + searchUrl + ' on ' + q)
		crawl(searchUrl, q)

