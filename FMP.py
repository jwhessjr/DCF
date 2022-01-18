import pandas as pd
from numpy import NaN
import certifi
import json
import requests
from urllib.request import urlopen
import hg_dcflib


def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode('utf-8')
    return json.loads(data)


url = ("https://financialmodelingprep.com/api/v3/cash-flow-statement/MYRG?period=quarter&limit=20&apikey=83968f6306c788e28e55925ceabc45e1")

data = get_jsonparsed_data(url)
# df = pd.json_normalize(data)
print(type(data))
# df = pd.json_normalize(data)
# print(data)
print()
print()
# print(data)
cshFlw = {}
depreciation = []
capex = []
indx = 0
for year in range(5):

    for qtr in range(indx+4):

        yearCapex = (data[indx]['capitalExpenditure'] + data[indx+1]
                     ['capitalExpenditure'] + data[indx+2]['capitalExpenditure'] + data[indx+3]['capitalExpenditure'])

        yearDeprec = (data[indx]['depreciationAndAmortization'] + data[indx+1]['depreciationAndAmortization'] +
                      data[indx+2]['depreciationAndAmortization'] +
                      data[indx+3]['depreciationAndAmortization'])
    capex.append(yearCapex)
    depreciation.append(yearDeprec)
    indx += 4
    if indx > 16:
        break

cshFlw['depreciation'] = depreciation
cshFlw['capex'] = capex
# def get_cshFlw(company):
# url = (
#     f'https://financialmodelingprep.com/api/v3/cash-flow-statement/MYRG?limit=5&apikey='+MYAPIKEY)
# data = get_jsonparsed_data(url)
# cshFlw = {}
# cshFlw['depreciation'] = [data[0]['depreciationAndAmortization'], data[1]['depreciationAndAmortization'],
#                           data[2]['depreciationAndAmortization'], data[3]['depreciationAndAmortization'], data[4]['depreciationAndAmortization']]
# cshFlw['capex'] = [data[0]['capitalExpenditure'], data[1]['capitalExpenditure'], data[2]
#                    ['capitalExpenditure'], data[3]['capitalExpenditure'], data[4]['capitalExpenditure']]

print(cshFlw)
# print(depreciation)
# print(capex)
# print(data[0]['sector'])
# print(type(df))
# print(df.iloc[0])
# print(df[['date', 'close']])

# data = get_jsonparsed_data(url)
# print(type(data))
# print(data)
# # print(data[0]['cik'])
