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

### moz_historyvisits
#0  id
#1  from_visit
#2  place_id
#3  visit_date
#4  visit_type
#5  session

class firefox_db:
    def __init__(self,history = 100):
        places = os.environ['APPDATA']+'\\Mozilla\\Firefox\\Profiles\\bpin7umv.default\\places.sqlite'
        self.db = sqlite3.connect(places)
        self.history = history

    def listHistory(self):
        q = 'SELECT id,url,title FROM moz_places ORDER BY id DESC LIMIT %d'
        q%= self.history
        r = self.db.execute(q)
        h = []
        for idx,url,title in r:
            if url.find('place:') == -1:
                for v in self.getVisits(idx):
                    h.append({
                        'id': idx,
                       'url': url.strip('http://'),
                     'title': title,
                      'time': str(v[3])
                        });
        return h[::-1]

    def getVisits(self,idx):
        q = "SELECT id,                         \
                    from_visit,                 \
                    place_id,                   \
                    visit_date                  \
             FROM moz_historyvisits             \
             WHERE place_id = %d"

        return self.db.execute(q%idx)
