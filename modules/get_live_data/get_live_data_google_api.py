import urllib2  # works fine with Python 2.7.9 (not 3.4.+)
import json
import time
import datetime
import pymongo
# stock_symbol = raw_input("Enter Stock Symbol : ")
# stock_indices = raw_input("Enter Stock Indices : ")

p0 = 0
class fetchstock():
    def fetchPreMarket(self,symbol, exchange,avg_time):
        try:
            while True :
                link = "http://finance.google.com/finance/info?client=ig&q="
                url = link+"%s:%s" % (exchange, symbol)
                try:
                    u = urllib2.urlopen(url)
                    if u is None:
                        print "No data"
                    else:
                        content = u.read()
                        data = json.loads(content[3:])
                        info = data[0]
                        current_price = info['l']
                        client = pymongo.MongoClient('localhost',27017)
                        db = client['Mohit_mongo']
                        collection = db["stockData"]
                        stock_list_avg=[]
                        try:
                            to_date = datetime.datetime.now().isoformat()
                            from_old_date = datetime.datetime.now() - datetime.timedelta(minutes=avg_time)
                            from_date = from_old_date.isoformat()
                            avg_data = collection.find(
                                            {'t': symbol,
                                            'lt_dts' : {
                                            '$lt': to_date,
                                            '$gte': from_date}})
                            for stock_each in avg_data:
                                stock_list_avg.append(stock_each['l'])
                            stock_list_avg.append(current_price)
                            stock_data_len = len(stock_list_avg)
                            total_stock_price = sum(map(float,stock_list_avg))
                            avg_stock_price = total_stock_price / stock_data_len
                            print avg_stock_price
                            
                        except Exception as e:
                            print e
                            pass
                        info["sma"] = avg_stock_price
                        try:
                            collection.insert(info)
                        except:
                            print "Document already exists"
                        time.sleep(1)
                except:
                    pass
                
#                 t = str(info["lt_dts"])
#                 if ',' in info["l"]:   # time stamp
#                     l_plain = info["l"].strip(',')
#                     l = float(l_plain)
#                 else:
#                     l = float(info["l"])    # close price (previous trading day)
#                 l_curr = info["l_cur"].split(';')
#                 if ',' in l_curr[1]:
#                     p_plain = l_curr[1].strip(',')
#                     p = float(p_plain)
#                 else:  
#                     p = float(l_curr[1])   # stock price in pre-market (after-hours)
#             
#                 time.sleep(1)
#             return (t,l,p)
        except Exception as e:
            print e
            pass

# p0 = 0
# while True:
#     t, l, p = fetchPreMarket(stock_symbol,stock_indices)
#     if(p!=p0):
#         p0 = p
#         print("%s\t%.2f\t%.2f\t%+.2f\t%+.2f%%" % (t, l, p, p-l,
#                                                  (p/l-1)*100.))
#         
#     time.sleep(1)