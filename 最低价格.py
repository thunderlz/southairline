import requests
import json
from datetime import datetime
import pandas as pd
from pandas import DataFrame,Series
import os

df=DataFrame()
date=datetime.now()
month=datetime.strftime(datetime.now(),'%Y-%m')
url='http://b2c.csair.com/portal/minPrice/queryMinPriceInMonth.ao'

headers={'Referer': 'http://b2c.csair.com/B2C40/modules/bookingnew/main/flightSelectDirect.html?t=S&c1=CAN&c2=CKG&d1=2018-04-29&at=1&ct=0&it=0',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
'X-Requested-With': 'XMLHttpRequest',
'Content-type':'application/json'}

d=lambda x:x['date']
p=lambda x:x['price']
airport=['CAN','CKG','SHA','PEK','CTU','SZX','PVG']
# airport=['CAN','CKG']
for dep in airport:
    for arr in airport:
        if dep!=arr:
            payload=json.dumps({"depCity":dep,"arrCity":arr,"month":month,"channel":"B2CPC1"})
            # time.sleep(2)
            rq=requests.post(url,headers=headers,data=payload)

            df_temp=pd.read_json(rq.text)
            df_temp['dep']=dep
            df_temp['arr']=arr
            df_temp['date']=df_temp['data'].apply(d)
            df_temp['price'] = df_temp['data'].apply(p)
            df=pd.concat([df,df_temp])
path='./最低价格/{}/'.format(datetime.strftime(datetime.now(),'%Y%m%d'))
if not os.path.exists(path):
    os.makedirs(path)
try:
    df.to_csv(path+'lowprice{}.csv'.format(date))
    print('执行成功！')
except:
    print('执行错误！')

