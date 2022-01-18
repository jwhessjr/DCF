"""This library is a collection of functions used in the Hess Group DCF model."""

import pandas as pd
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import certifi
import json

# Read statements from Financial Modeling Prep


def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode('utf-8')
    return json.loads(data)

# Function to get the income statement and extract the required fields


def get_incStmnt(company, MYAPIKEY):
    url = (
        f'https://financialmodelingprep.com/api/v3/income-statement/{company}?period=quarter&limit=20&apikey='+MYAPIKEY)
    data = get_jsonparsed_data(url)
    incStmnt = {}

    incStmnt['netIncome'] = data[0]['netIncome'], \
        data[1]['netIncome'],\
        data[2]['netIncome'], \
        data[3]['netIncome'], \
        data[4]['netIncome']
    incStmnt['interestIncome'] = [data[0]['interestIncome'],
                                  data[1]['interestIncome'],
                                  data[2]['interestIncome'],
                                  data[3]['interestIncome'],
                                  data[4]['interestIncome']]

    incStmnt['totalRevenue'] = [data[0]['revenue'], data[1]['revenue']]
    incStmnt['incomeBeforeTax'] = data[0]['incomeBeforeTax']
    incStmnt['ebit'] = [data[0]['operatingIncome'],
                        data[1]['operatingIncome'],
                        data[2]['operatingIncome'],
                        data[3]['operatingIncome'],
                        data[4]['operatingIncome']]

    return incStmnt

# Function to get the balance sheet and extract the required fields


def get_balSht(company, MYAPIKEY):
    url = (
        f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{company}?period=quarter&limit=8&apikey='+MYAPIKEY)
    data = get_jsonparsed_data(url)
    balSht = {}
    balSht['cashAndCashEquivalents'] = \
        [data[0]['cashAndCashEquivalents'], data[1]['cashAndCashEquivalents']]
    balSht['totalCurrentAssets'] = \
        [data[0]['totalCurrentAssets'],
         data[1]['totalCurrentAssets']]
    balSht['totalCurrentLiabilities'] = \
        [data[0]['totalCurrentLiabilities'], data[1]['totalCurrentLiabilities']]
    balSht['totalLiabilities'] = \
        [data[0]['totalLiabilities'],
         data[1]['totalLiabilities']]
    balSht['totalStockholdersEquity'] = \
        [data[0]['totalStockholdersEquity'], data[1]['totalStockholdersEquity']]

    return balSht

# Function to get the cash flow statement and extract the required fields


def get_cshFlw(company, MYAPIKEY):
    url = (
        f'https://financialmodelingprep.com/api/v3/cash-flow-statement/{company}?period=quarter&limit=20&apikey='+MYAPIKEY)
    data = get_jsonparsed_data(url)
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

    return cshFlw

# Function to extract number of shares outstanding


def get_entVal(company, MYAPIKEY):
    url = (
        f'https://financialmodelingprep.com/api/v3/enterprise-values/{company}?limit=1&apikey='+MYAPIKEY)
    data = get_jsonparsed_data(url)
    sharesOutstanding = data[0]['numberOfShares']

    return sharesOutstanding

# Function to get the current share price


def get_price(company, MYAPIKEY):
    url = (
        f'https://financialmodelingprep.com/api/v3/quote-short/{company}?apikey='+MYAPIKEY)
    data = get_jsonparsed_data(url)
    price = data[0]['price']

    return price


def get_riskFree():
    url = 'https://www.cnbc.com/quotes/US10Y'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    result = soup.find(class_="QuoteStrip-lastPrice")
    riskFree = float(result.text[:-1])/100
    # print(f'Risk Free Rate {riskFree}')
    return riskFree


def get_industry(company):
    indName = pd.read_excel(
        '/Users/jhess/Development/DCF/DCF/indname.xlsx', sheet_name='US by industry')
    for index, row in indName.iterrows():
        try:
            if company == row['Exchange:Ticker'].split(':')[1]:
                industry = row['Industry Group']
                print(f'Industry Group {industry}')
            else:
                continue
        except TypeError:
            continue
        except AttributeError:
            continue
    return industry


def get_beta(industry):
    beta = pd.read_excel(
        '/Users/jhess/Development/DCF/DCF/betas-3.xlsx', sheet_name='Industry Averages')
    for index, row in beta.iterrows():
        try:

            if industry in row['Industry Name']:
                unleveredBeta = row['Unlevered beta corrected for cash']
            else:
                continue
        except TypeError:
            continue
    print(f'Beta {unleveredBeta}')
    return unleveredBeta
