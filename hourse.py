#!/usr/bin/env python
#

# Import libraries
import os
import sys
import subprocess

sys.path.append('./lib')

from dbs import firefox_db


class Hourse:
	def __init__(self):
		self.db = firefox_db()
		self.history = self.db.listHistory()


if __name__ == "__main__":
	g = Hourse()