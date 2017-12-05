from nsetools import Nse
from pprint import pprint
import json
import pymongo
import threading
from datetime import datetime, time
import itertools

def stock_data_thread(stock):
    nse = Nse()
    data = nse.get_quote(stock)
    symbol = data['symbol']    
    client = pymongo.MongoClient('localhost',27017)
    db = client['rm_analysis']
    collection = db[symbol]
    for i in itertools.count():
        now = datetime.now()
        now_time = now.time()
        print now_time
        if now_time >= time(9,30) and now_time <= time(15,30):
            nse = Nse()
            data = nse.get_quote(stock)
            current_date_time = datetime.now()
            data['m_recorded_date_time']= current_date_time
            try:
                collection.insert(data)
                print "Data Entered In DB"
            except:
                print "Document already exists"
        else:
            print "Terminal Closed"


stock_data_thread('infy')