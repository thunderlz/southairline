import requests
import json
import time
import pandas as pd
from pandas import DataFrame,Series
from datetime import datetime
import time

def datelist(beginDate, endDate):
    # beginDate, endDate是形如‘20160601’的字符串或datetime格式
    date_l=[datetime.strftime(x,'%Y%m%d') for x in list(pd.date_range(start=beginDate, end=endDate))]
    return date_l

def FindFlight(s,dep,arr,date,headers,proxie):
    data = {'json': '{"depCity\":"' + dep + '\", "arrCity":\"' + arr + '\", "flightDate":\"' + date + '\", "adultNum":"1", "childNum":"0", "infantNum":"0", "cabinOrder":"0", "airLine":"1", "flyType":"0", "international":"0", "action":"0", "segType":"1", "cache":"1", "preUrl":"", "isMember":""}'}
    print(s.get('http://b2c.csair.com/B2C40/newTrips/static/main/page/booking/index.html?t=S&c1=CAN&c2=CKG&d1=2018-11-16&at=1&ct=0&it=0').status_code)
    time.sleep(6)
    rq = s.post(url, headers=headers, data=data,proxies=proxie)
    if rq.status_code==200:
        try:
            print(rq.text)
            flights = json.dumps(json.loads(rq.text)['segment']['dateflight']['flight'])
            return flights
        except:
            print( dep+ '-->' + arr + ' ' + date + '之间没有航班。')
            return json.dumps({})
    else:
        print(rq.status_code)
        return -1


df=DataFrame()

url='http://b2c.csair.com/B2C40/query/jaxb/direct/query.ao'

headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
'Accept': 'pplication/json, text/javascript, */*; q=0.01',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Connection': 'keep-alive',
# 'Content-Length': '227',
'Content-Type': 'application/json',
'Host': 'b2c.csair.com',
'Origin': 'http://b2c.csair.com'
}

datelist=datelist('20181117','20181231')
print(datelist)
airport=['CKG','SHA','PEK','CTU','PVG']
# airport=['CAN','CKG']
# proxie={'http':'http://27.40.148.69:61234',
#         'https':'http://27.40.148.69:61234'
#         }
proxie={}
s=requests.session()

for date in datelist:
    # for dep in airport:
    dep='CAN'
    for arr in airport:
        if dep!=arr:
            flights=FindFlight(s,dep,arr,date,headers,proxie)
            if flights==-1:
                exit(0)
            print(flights)
            df_temp = pd.read_json(flights)
            if len(df)==0:
                df=df_temp
            else:
                df=pd.concat([df,df_temp])

df.to_csv('flights{}.csv'.format(datetime.now().strftime('%y%m%d%H%M')))