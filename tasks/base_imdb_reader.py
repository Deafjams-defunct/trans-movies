import re
import os
import sys 
reload(sys) 
sys.setdefaultencoding("utf-8")

import pymongo

def main():
    
    mongo = pymongo.MongoClient(os.environ.get('MONGOLAB_URI'))['heroku_1s6ngsfg']
    mongo.movies.ensure_index('title', background=True)
    with open(os.path.join('data', 'release-dates.list')) as release_dates_file:
        
        data_started = False
        for line in release_dates_file:
            
            if line == '==================\n':
                data_started = True
                continue
                
            if not data_started:
                continue
                
            line = line.split('\t')
            if '{' in line[0]:
                bracket = line[0].index('{')
                title = line[0][:bracket]
            
            else:
                title = line[0]
                
            quote_index = title.rindex('"')
            year = title[quote_index + 1:].strip()
            title = title[1:quote_index]
            
            
            title = '{} {}'.format(title, year)
            
            record = {'title': title.decode('latin-1').encode('utf-8')}
            
            if not mongo.movies.find(record, limit=1).count():
                mongo.movies.insert(record)
    
if __name__ == '__main__':
    main()