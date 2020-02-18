import requests
import json
import pickle
from datetime import datetime as dt
import pandas as pd
import time

from sqlalchemy import create_engine
from sqlalchemy.types import JSON

class southairticket:
    def __init__(self,depCity,arrCity):
        self.url='https://b2c.csair.com/portal/flight/direct/query'
        self.headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        # 'Host': 'b2c.csair.com',
        'Content-type':'application/json'
        }
        self.data={"depCity":depCity,"arrCity":arrCity,"flightDate":dt.now().strftime('%Y%m%d'),"adultNum":"1","childNum":"0","infantNum":"0",
                 "cabinOrder":"0","airLine":1,"flyType":0,
                 "international":"0","action":"0","segType":"1","cache":0,"preUrl":"MIP002","isMember":""}
        self.session=requests.Session()
        self.engine = create_engine('mysql+pymysql://root:751982THUNDERlz@localhost:3306/saflights')


        
    def getjson(self,getdate):
        self.data['flightDate']=getdate
        for i in range(3):
            time.sleep(10)
            for j in range(3):
                try:
                    self.resp=self.session.post(url=self.url,headers=self.headers,data=json.dumps(self.data),timeout=20)
                    break
                except:
                    print('20 second timeout')
            if json.loads(self.resp.content)['success']==True:
#                 with open('{}-{}执行时间{}票价时间{}.json'.format(self.data['depCity'],self.data['arrCity'],dt.now().strftime('%Y%m%d%H%M'),getdate),'wb') as f:
#                     pickle.dump(self.resp.content,f)
                self.savesql(self.resp.content)
                print(getdate,'ok')
                break
            else:
                print(getdate,'error')
        
    def getPieriods(self,sdate,ndays):
        for getdate in pd.date_range(sdate,periods=ndays):
            self.getjson(getdate.strftime('%Y%m%d'))
            
    def savesql(self,content):
        df=pd.read_json(json.dumps(json.loads(content)['data']['segment'][0]['dateFlight']['flight']))
        df['allprice']=df.apply(lambda x:str({x['name']:x['adultPrice'] for x in  x['cabin']}),axis=1)
        df['lowprice']=df.apply(lambda x:self.mymin([x['adultPrice'] for x in  x['cabin']]),axis=1)
        df['querydate']=dt.now().strftime('%Y%m%d%H%M')
#         df.drop(['cabin'],axis=1,inplace=True)
#         df['cabin']=df['cabin'].apply(str)
        df.to_sql(name='flights',con=self.engine,if_exists='append',dtype={'cabin':JSON})
        
    def mymin(self,sequence):
        if len(sequence)>0:
            return min(sequence)
        else:
            return 0
            
if __name__ == '__main__':
    sat=southairticket('CAN','PEK')
    sat.getPieriods(dt.now().strftime('%Y%m%d'),60)

