#!/usr/bin/env python
#

# Import libraries
import os
import sys
import subprocess
import unicodedata

sys.path.append('./lib')

from dbs import firefox_db


class Hourse:
	def __init__(self):
		self.db = firefox_db()
		self.history = self.db.getVisits(16)
		for f in self.history:
			print f
		#self.createCustomLog()
		#self.launchGource()

	def createCustomLog(self):

		self.log = ''

		for r in self.history:
			self.log+= '|'.join([
								'Firefox',
								'M',
								self.noUni(r['url']),
								'default',
								self.noUni(r['title'])
							   ])+"\n"

	def launchGource(self):
		gource = subprocess.Popen(['gource', 
									 '--log-format', 'custom', 
									 '--hide', 'progress',
									 '-i', '0', 
									 '-a','1', 
									 '--realtime',
									 '-', self.log], 
									 shell=True)
		gource.communicate()



	def noUni(self,instr):
		return unicodedata.normalize('NFKD', instr).encode('ascii','ignore')


if __name__ == "__main__":
	main = Hourse()
