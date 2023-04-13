
import requests as re
import os
import json
import pandas as pd

#base_url = 'https://api.iex.cloud/v1/'
#api_token = '?token=' + os.environ["API_KEY"]
#quote = re.get(base_url + '/data/core/quote/aapl' + api_token)

os.chdir(r"D:\Data")
df = pd.read_csv("original.csv", header=0)


print(df.head())

