from nsetools import Nse
from pprint import pprint
import json
import pymongo
import threading
from datetime import datetime, time
import itertools
import thread
import json

def stock_data_thread(thread_name,stock):
    nse = Nse()
    data = nse.get_quote(stock)
    symbol = data['symbol']
    client = pymongo.MongoClient('localhost',27017)
    db = client['rm_analysis']
    collection = db[symbol]
    for i in itertools.count():
        now = datetime.now()
        now_time = now.time()
        if now_time >= time(9,30) and now_time <= time(15,30):
            nse = Nse()
            try:
                data = nse.get_quote(stock)
            except IOError as e:
                print "I/O error({0}): {1}".format(e.errno, e.strerror)
                pass
            current_date_time = datetime.now()
            data['m_recorded_date_time']= current_date_time
            try:
                collection.insert(data)
                print str(symbol) + "---Data Entered In DB ---" + str(now_time)
            except:
                print "Document already exists"
        else:
            print "Terminal Closed"

def multi_thread_stock_data():
    testbed_data = json.load(open('/Users/zymr/Workspace/NSE_Grabbing/config/base_data/nse_top_100.json'))
    print testbed_data
    stock_list= testbed_data["nse_top_100"]
    print stock_list
    thread_counter= 0
    try:
        for each_stock in stock_list:
            thread_counter= thread_counter+1
            thread_name= "Thread-" + str(thread_counter)
            thread.start_new_thread(stock_data_thread, ("thread_name",str(each_stock)))
            print thread_name + "started"
    except:
        print "Unable to start thread"
    while 1:
        pass
multi_thread_stock_data()