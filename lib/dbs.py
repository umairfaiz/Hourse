import os
import sys
import shutil
import sqlite3 # Needs 3.7.17
import unicodedata

class database(object):

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

    def listHistory(self): raise NotImplementedError

    def getVisits(self): raise NotImplementedError



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
        shutil.copy2(places,'./dbs/Firefox.db')
        self.db = sqlite3.connect('./dbs/Firefox.db')
        self.browser = 'Firefox'
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
                      'time': str((v[3]/1000000)),
                   'browser':self.browser
                        });
        return sorted(h, key=lambda k: k['time'])

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
        shutil.copy2(places,'./dbs/Chrome.db')
        self.db = sqlite3.connect('./dbs/Chrome.db')
        self.browser = 'Chrome'
        self.history = history

    def listHistory(self):
        q = 'SELECT id,url,title FROM urls ORDER BY id DESC LIMIT %d'
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
                      'time': str((v[0]/1000000)-11644473600),
                   'browser':self.browser
                        });
        return sorted(h, key=lambda k: k['time'])

    def getVisits(self,url):
        q = 'SELECT visit_time,url,from_visit FROM visits WHERE url = %s'
        q%=url
        return self.db.execute(q)



class both_db(database):
    def __init__(self,history=1000):
        self.history = history

    def listHistory(self):
        c = chrome_db(self.history)
        f = firefox_db(self.history)
        c = c.listHistory()
        f = f.listHistory()
        return sorted(c+f, key=lambda k: k['time'])