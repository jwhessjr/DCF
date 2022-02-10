"""This library is a collection of functions used in the Hess Group DCF model."""

from operator import indexOf
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


def get_incStmnt(company, myApiKey):
    url = (
        f'https://financialmodelingprep.com/api/v3/income-statement/{company}?period=quarter&limit=20&apikey='+myApiKey)
    data = get_jsonparsed_data(url)
    incStmnt = {}
    netIncome = []
    interestIncome = []
    totalRevenue = []
    incomeBeforeTax = []
    incomeTaxExpense = []
    ebit = []
    indx = 0
    for year in range(5):
        for qtr in range(indx+4):
            yearNetIncome = (data[indx]['netIncome'] + data[indx+1]['netIncome'] +
                             data[indx+2]['netIncome'] + data[indx+3]['netIncome'])

            yearIntIncome = (data[indx]['interestIncome'] + data[indx+1]['interestIncome'] +
                             data[indx+2]['interestIncome'] + data[indx+3]['interestIncome'])

            yearTotalRevenue = (data[indx]['revenue'] + data[indx+1]['revenue'] +
                                data[indx+2]['revenue'] + data[indx+3]['revenue'])

            yearIncBeforeTax = (data[indx]['incomeBeforeTax'] + data[indx+1]['incomeBeforeTax'] +
                                data[indx+2]['incomeBeforeTax'] + data[indx+3]['incomeBeforeTax'])

            yearTaxExpense = (data[indx]['incomeTaxExpense'] + data[indx+1]['incomeTaxExpense'] +
                              data[indx+2]['incomeTaxExpense'] + data[indx+3]['incomeTaxExpense'])

            yearEbit = (data[indx]['operatingIncome'] + data[indx+1]['operatingIncome'] +
                        data[indx+2]['operatingIncome'] + data[indx+3]['operatingIncome'])

        netIncome.append(yearNetIncome)
        interestIncome.append(yearIntIncome)
        totalRevenue.append(yearTotalRevenue)
        incomeBeforeTax.append(yearIncBeforeTax)
        incomeTaxExpense.append(yearTaxExpense)
        ebit.append(yearEbit)
        indx += 4
        if indx > 16:
            break
    incStmnt['netIncome'] = netIncome
    incStmnt['interestIncome'] = interestIncome
    incStmnt['totalRevenue'] = totalRevenue
    incStmnt['incomeBeforeTax'] = incomeBeforeTax
    incStmnt['incomeTaxExpense'] = incomeTaxExpense
    incStmnt['ebit'] = ebit

    return incStmnt


# Function to get the balance sheet and extract the required fields


def get_balSht(company, myApiKey):
    url = (
        f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{company}?period=quarter&limit=8&apikey='+myApiKey)
    data = get_jsonparsed_data(url)
    balSht = {}
    cashAndEquivalents = [data[0]['cashAndShortTermInvestments'],
                          data[4]['cashAndShortTermInvestments']]
    currentAssets = [data[0]['totalCurrentAssets'],
                     data[4]['totalCurrentAssets']]
    accountsPayable = [
        data[0]['accountPayables'], data[4]['accountPayables']]
    stockholdersEquity = [
        data[0]['totalStockholdersEquity'], data[4]['totalStockholdersEquity']]
    liabilities = [data[0]['totalLiabilities'], data[4]['totalLiabilities']]
    shortTermDebt = [data[0]['shortTermDebt'], data[4]['shortTermDebt']]

    balSht['cashAndCashEquivalents'] = cashAndEquivalents
    balSht['totalCurrentAssets'] = currentAssets
    balSht['accountsPayable'] = accountsPayable
    balSht['totalLiabilities'] = liabilities
    balSht['shortTermDebt'] = shortTermDebt
    balSht['totalStockholdersEquity'] = stockholdersEquity

    return balSht


# Function to get the cash flow statement and extract the required fields


def get_cshFlw(company, myApiKey):
    url = (
        f'https://financialmodelingprep.com/api/v3/cash-flow-statement/{company}?period=quarter&limit=20&apikey='+myApiKey)
    data = get_jsonparsed_data(url)
    cshFlw = {}
    depreciation = []
    capex = []
    acquisition = []
    indx = 0
    for year in range(5):

        for qtr in range(indx+4):

            yearCapex = (data[indx]['capitalExpenditure'] + data[indx+1]
                         ['capitalExpenditure'] + data[indx+2]['capitalExpenditure'] + data[indx+3]['capitalExpenditure'])

            yearDeprec = (data[indx]['depreciationAndAmortization'] + data[indx+1]['depreciationAndAmortization'] +
                          data[indx+2]['depreciationAndAmortization'] +
                          data[indx+3]['depreciationAndAmortization'])
            yearAcquisition = (data[indx]['acquisitionsNet'] + data[indx+1]['acquisitionsNet'] +
                               data[indx+2]['acquisitionsNet'] + data[indx+3]['acquisitionsNet'])
        capex.append(yearCapex)
        depreciation.append(yearDeprec)
        acquisition.append(yearAcquisition)
        indx += 4
        if indx > 16:
            break

    cshFlw['depreciation'] = depreciation
    cshFlw['capex'] = capex
    cshFlw['acquisition'] = acquisition

    return cshFlw

# Function to extract number of shares outstanding


def get_entVal(company, myApiKey):
    url = (
        f'https://financialmodelingprep.com/api/v3/enterprise-values/{company}?limit=1&apikey='+myApiKey)
    data = get_jsonparsed_data(url)
    sharesOutstanding = data[0]['numberOfShares']
    marketCap = data[0]['marketCapitalization']
    entVal = sharesOutstanding, marketCap

    return entVal

# Function to get the current share price


def get_price(company, myApiKey):
    url = (
        f'https://financialmodelingprep.com/api/v3/quote-short/{company}?apikey='+myApiKey)
    data = get_jsonparsed_data(url)
    price = data[0]['price']

    return price


def get_riskFree():
    url = 'https://www.cnbc.com/quotes/US10Y'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    result = soup.find(class_="QuoteStrip-lastPrice")
    riskFree = float(result.text[:-1])/100
    print(f'Risk Free Rate {riskFree}')
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
                unleveredBeta = row['Unlevered beta']
            else:
                continue
        except TypeError:
            continue
    print(f'Beta {unleveredBeta}')
    return unleveredBeta
