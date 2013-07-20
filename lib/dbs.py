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
    def __init__(self,history = 100):
        self.db = sqlite3.connect('C:\\Users\\Travis\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\bpin7umv.default\\places.sqlite')

    def listHistory(self):
        q = 'SELECT id,url,title FROM moz_places ORDER BY id DESC LIMIT %d'
        q%= history
        r = self.db.execute(q)
        h = []
        for idx,url,title in r:
            if url.find('place:') == -1:
                h.append({
                    'id': idx,
                   'url': url,
                 'title': title if title else url
                    });
        return h

    def getVisits(self,idx):
        q = "SELECT id,                         \
                    from_visit,                 \
                    place_id,                   \
                    visit_date                  \
             FROM moz_historyvisits             \
             WHERE place_id = %d"

        return self.db.execute(q%idx)
