import streamlit as st
import config
from iex import IEXStock
import pandas as pd
import redis
import json
from datetime import timedelta

redis_client = redis.Redis(host='localhost', port=6379, db=0)

sym = st.text_input("Symbol", value='AAPL')
symbol = sym.lower()

stock = IEXStock(config.my_key, symbol)

# pulls information from redis cache
company_info_key = f"{symbol}_company_info"
company_info = redis_client.get(company_info_key)

if company_info is None:
    print("Not in cache. Making API call ...")
    company_info = stock.get_company_info()
    # converts back into json string (not dictionary as returned by API)
    redis_client.set(company_info_key, json.dumps(company_info))
    redis_client.expire(company_info_key, timedelta(seconds=30))

else:
    print("Found in cache, retrieving ...")
    company_info = json.loads(company_info)

st.subheader('Company Name:')
st.write(company_info['companyName'])
st.subheader('Exchange:')
st.write(company_info['exchange'])


stats = stock.get_historical_prices()
st.write(json.dumps(stats))

# df = pd.DataFrame.from_dict(stats)
# print(df['open'])
