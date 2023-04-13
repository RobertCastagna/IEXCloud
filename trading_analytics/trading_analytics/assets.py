
import requests as re
import os
import json
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

base_url = 'https://sandbox.iexapis.com/v1'
api_token = '?token=' + os.getenv('API_KEY')

quote = re.get(base_url + '/stock/aapl/quote' + api_token)

#os.chdir(r"D:\Data")
#df = pd.read_csv("original.csv", header=0)
#print(df.head())
