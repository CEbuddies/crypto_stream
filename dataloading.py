# fetching data function
# author: nic
from requests import Request, Session
import pandas as pd
import json
from datetime import datetime

def fetch_data(nums,key):
    #### Data Fetching Block
    # fetch data
    start = nums[0]
    end = nums[1]
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    # param dict - we want euros instead of USD (change accordingly)
    parameters = {
                  'start':start,
                  'limit':end,
                  'convert':'EUR'
        }
    # limit - how many currencies are being read 
    # - so far seems to only cost one token per call anyway 
    # here the key must be inserted ! (access via the website)
    headers = {
              'Accepts': 'application/json',
              'X-CMC_PRO_API_KEY': key,
                }

    # create session object to pass in the header
    # - mayber later expand this with try and catch
    session = Session()
    session.headers.update(headers)
    
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    now = datetime.now()
    timestamp = now.strftime('%H:%M - %b %d')
    # maybe write the status stuff to the file 
    with open('data.lck','w') as wl:
        wl.write(timestamp)
    bulk_data = data['data']
    mc, prices = process_quote(bulk_data)
    # maybe process json here
    df_cr = pd.DataFrame(bulk_data)
    df_cr['price'] = prices
    df_cr['market cap'] = mc
    # drop the extra index column
    df_cr.reset_index(drop=True,inplace=True)
    df_cr.to_pickle('bulk_data_last.ccf')

    return df_cr

def load_data():
    df_cr = pd.read_pickle('bulk_data_last.ccf')
    df_cr.reset_index(drop=True,inplace=True)
    
    with open('data.lck') as dl:
        from_time = dl.read()
    return df_cr, from_time

def process_quote(data):
    
    market_cap = []
    price = []
    for el in data:
        
        dd = el['quote']
        market_cap.append(dd['EUR']['market_cap'])
        price.append(dd['EUR']['price'])
    
    return market_cap, price

def get_key(path):

    with open(path,'r') as kf:
        API = kf.read()
    API = API.strip('\n')

    return API


