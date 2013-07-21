#!/usr/bin/env python
#

# Import libraries
import os
import sys
import random
from subprocess import call

sys.path.append('./lib')

from dbs import *


class Hourse:
	def __init__(self):
		#self.db = chrome_db()
		self.db = firefox_db()
		self.history = self.db.listHistory()
		# 
		# self.createCustomLog()
		# self.launchGource()

	def createCustomLog(self):
		self.log = ''

		for r in self.history:
			self.log+= '|'.join([
								r['time'],
								'Firefox',
								'M',
								r['url'],
								self.getColor(r['url']),
								r['title']
							   ])+"\n"

		f = open('log.tmp','wb')
		f.write(self.log)


	def launchGource(self):
		call(['gource', 
				 '--hide', 'progress',
				 '-i', '0', 
				 '-a', '1', 
				 'log.tmp'])

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
	main = Hourse()
