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
		self.history = self.db.listHistory()
		self.createCustomLog()
		self.launchGource()

	def createCustomLog(self):
		self.log = ''

		for r in self.history:
			self.log+= '|'.join([
								r['time'],
								'Firefox',
								'M',
								self.noUni(r['url']),
								'#FF0000',
								self.noUni(r['title'])
							   ])+"\r\n"

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
		if instr:
			return unicodedata.normalize('NFKD', instr).encode('ascii','ignore')
		else:
			return ' '


if __name__ == "__main__":
	main = Hourse()
