import pandas as pd
from numpy import NaN
import certifi
import json
import requests
from urllib.request import urlopen


def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode('utf-8')
    return json.loads(data)


url = ("https://financialmodelingprep.com/api/v3/income-statement/HRTG?limit=5&apikey=83968f6306c788e28e55925ceabc45e1")

data = get_jsonparsed_data(url)
# df = pd.json_normalize(data)
print(type(data))
# df = pd.json_normalize(data)
# print(data)
print()
print()
print(data)
# print(data[0]['sector'])
# print(type(df))
# print(df.iloc[0])
# print(df[['date', 'close']])

# data = get_jsonparsed_data(url)
# print(type(data))
# print(data)
# # print(data[0]['cik'])
