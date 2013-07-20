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
								'',
								self.noUni(r['title'])
							   ])+"\n"

		f = open('log.tmp','wb')
		f.write(self.log)


	def launchGource(self):
		gource = subprocess.Popen(['gource', 
									 '--hide', 'progress',
									 '-i', '0', 
									 '-a','1', 
									 'log.tmp'], 
									 shell=True,
									 stdin = sys.__stdout__)
		gource.communicate()


	def noUni(self,instr):
		if instr:
			return unicodedata.normalize('NFKD', instr).encode('ascii','ignore')
		else:
			return ' '


if __name__ == "__main__":
	main = Hourse()
