#!/usr/bin/env python
#

# Import libraries
import os
import sys
import random
from subprocess import call

sys.path.append('./lib')

from dbs import *


class Hourse(object):

	def __init__(self,browser):
		self.browser = browser

		if browser == 'Chrome':
			self.db = chrome_db(1000)
		elif browser == 'Firefox':
			self.db = firefox_db(1000)
		elif browser == 'Both':
			self.db = both_db(1000)


		self.history = self.db.listHistory()
		self.createCustomLog()
		self.launchGource()

	def createCustomLog(self):
		self.log = ''

		for r in self.history:
			self.log+= '|'.join([
								r['time'],
								r['browser'],
								'M',
								r['url'],
								self.getColor(r['url']),
								r['title']
							   ])+"\n"

		f = open('log/history.hrc','wb')
		f.write(self.log)


	def launchGource(self):
		call(['gource', 
				 '--hide', 'progress,dirnames,filenames',
				 '-i', '0', 
				 '-a', '1', 
				 'log/history.hrc'])

	def getColor(self,url):
		r = hex(random.randrange(200,255,1))[-2:]
		g = hex(random.randrange(200,255,1))[-2:]
		b = hex(random.randrange(200,255,1))[-2:]
		o = r+g+b

		if url.find('imgur.com') > -1:
			o = '85BF25'
		elif url.find('reddit.com') > -1:
			o = 'FFFFFF'
		elif url.find('wikipedia.org') > -1:
			o = '6666CC'
		elif url.find('facebook.com') > -1:
			o = '4C66A4'

		return o

if __name__ == "__main__":
	main = Hourse('Both')
