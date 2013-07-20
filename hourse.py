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

	def createCustomLog(self):
		self.log = ''

		for r in self.history:
			self.log+= '|'.join([
								'Firefox',
								'M',
								self.noUni(r['url']),
								'default',
								self.noUni(r['title'])
							   ])+"\r\n\r\n\r\n"

		print self.log

	def noUni(self,instr):
		return unicodedata.normalize('NFKD', instr).encode('ascii','ignore')


if __name__ == "__main__":
	main = Hourse()
