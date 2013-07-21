import os
import sys
import shutil
import sqlite3 # Needs 3.7.17
import unicodedata



class database(object):

    def listHistory(self): raise NotImplementedError

    def getVisits(self): raise NotImplementedError

    def strip(self,url,dist=5):
        strip = ['http://','https://']
        for s in strip:
            url = url.strip(s)

        f = url.find('.')
        if f < dist:
            url = url[f+1:]

        return url

    def noUni(self,instr):
        if instr:
            return unicodedata.normalize('NFKD', instr).encode('ascii','ignore')
        else:
            return ' '


###
### Firefox Database
######################

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

class firefox_db(database):
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
                url = self.strip(self.noUni(url))
                suf = url[:url.find('.')]
                url+='.'+suf

                for v in self.getVisits(idx):
                    h.append({
                        'id': idx,
                       'url': url,
                     'title': self.noUni(title) if title else url,
                      'time': str((v[3]/1000000))
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


###
### Chrome Database
####################

### urls
#0  id
#1  url
#2  title
#3  visit_count
#4  typed_count
#5  last_visit_time
#6  hidden
#7  favicon_id

### visits
#0  id
#1  url
#2  visit_time
#3  from_visit
#4  transition
#5  segment_id
#6  is_indexed
#7  visit_duration

### visit_source
#0  id
#1  source

class chrome_db(database):
    def __init__(self,history = 100):
        places = os.path.dirname(os.environ['APPDATA']) # APPDATA puts us in roaming, pop up a dir
        places+='\\Local\\Google\\Chrome\\User Data\\Default\\History'
        shutil.copy2(places,'./dbs/Chrome')
        self.db = sqlite3.connect('./dbs/Chrome')
        self.history = history

    def listHistory(self):
        pass