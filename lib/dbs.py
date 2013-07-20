
import os
import sys
import sqlite3 # Needs 3.7.17

### moz_places:
#0  id
#1  url
#2  title
#3  rev_host
#4  visit_count
#5  hidden
#6  typed
#7  favicon_id
#8  frecency [sic]
#9  last_visit_date
#10 guid

class firefox_db:
    def __init__(self):
        self.db = sqlite3.connect('C:\\Users\\Travis\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\bpin7umv.default\\places.sqlite')
        self.listHistory()

    def listHistory(self,history = 100):
        r = self.db.execute('SELECT id,url,title FROM moz_places ORDER BY id DESC LIMIT %d'%history)
        h = []
        for idx,url,title in r:
            h.append({
                'id': idx,
               'url': url,
             'title': title if title else url
                });
        return h
