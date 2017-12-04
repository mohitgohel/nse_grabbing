from nsetools import Nse
from pprint import pprint
import json
import pymongo
import threading
import datetime
name = raw_input('Enter Stock Symbol : ')

def stock_data_thread():
    threading.Timer(5.0,stock_data_thread).start()
    nse = Nse()
    data = nse.get_quote(name)
#     pprint(data)
#     print data['lastPrice']
    symbol = data['symbol']
    current_date_time = datetime.datetime.now()
    data['m_recorded_date_time']= current_date_time
    
    ### Mongo conneciton ###
    
    client = pymongo.MongoClient('localhost',27017)
    db = client['Mohit_mongo']
    collection = db[symbol]
    try:
        collection.insert(data)
    except:
        print "Document already exists"

stock_data_thread()