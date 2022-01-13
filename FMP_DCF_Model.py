#!/usr/bin/env python
# coding: utf-8

# # DCF Model Using Financial Modeling Prep Inputs


# import required libraries

import pandas as pd
import certifi
import json
from urllib.request import urlopen
import sqlite3
from sqlite3 import Error
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import xlrd
import openpyxl


# read statements from FMP


def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode('utf-8')
    return json.loads(data)


# Function to get the income statement and extract the required fields
def get_incStmnt(company):
    url = (
        f'https://financialmodelingprep.com/api/v3/income-statement/{company}?limit=5&apikey=83968f6306c788e28e55925ceabc45e1')
    data = get_jsonparsed_data(url)
    incStmnt = {}

    incStmnt['netIncome'] = data[0]['netIncome'], data[1]['netIncome'],\
        data[2]['netIncome'], data[3]['netIncome'], data[4]['netIncome']
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
def get_balSht(company):
    url = (
        f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{company}?limit=2&apikey=83968f6306c788e28e55925ceabc45e1")
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
def get_cshFlw(company):
    url = (
        f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{company}?limit=5&apikey=83968f6306c788e28e55925ceabc45e1")
    data = get_jsonparsed_data(url)
    cshFlw = {}
    cshFlw['depreciation'] = [data[0]['depreciationAndAmortization'], data[1]['depreciationAndAmortization'],
                              data[2]['depreciationAndAmortization'], data[3]['depreciationAndAmortization'], data[4]['depreciationAndAmortization']]
    cshFlw['capex'] = [data[0]['capitalExpenditure'], data[1]['capitalExpenditure'], data[2]
                       ['capitalExpenditure'], data[3]['capitalExpenditure'], data[4]['capitalExpenditure']]

    return cshFlw


# Function to extract number of shares outstanding
def get_entVal(company):
    url = (
        f"https://financialmodelingprep.com/api/v3/enterprise-values/{company}?limit=1&apikey=83968f6306c788e28e55925ceabc45e1")
    data = get_jsonparsed_data(url)
    sharesOutstanding = data[0]['numberOfShares']

    return sharesOutstanding

# Function to get the current share price


def get_price(company):
    url = (
        f"https://financialmodelingprep.com/api/v3/quote-short/{company}?apikey=83968f6306c788e28e55925ceabc45e1")
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
            if company in row['Exchange:Ticker']:
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


def main():
    company = input('Input company ticker: ').upper()
    print(company)
    EQPREM = .0490
    industry = get_industry(company)
    unleveredBeta = get_beta(industry)
    riskFree = get_riskFree()
    growthPeriod = int(input('Input growth period: '))
    stableGrowth = float(input('Input growth rate for stable period: '))
    StableEqRe = float(input('Input stable period equity reinvestment rate: '))
    stableBeta = float(input('Input stable period beta: '))

    incStmnt = get_incStmnt(company)
    # print(type(incStmnt))
    # print(incStmnt)
    # print(incStmnt[0]['netIncome'])

    # print('----------------------------------------------------')

    balSht = get_balSht(company)
    # print(type(balSht))
    # print(balSht)
    # print(balSht[0]['totalCurrentLiabilities'])
    # print('-----------------------------------------------------')

    cshFlw = get_cshFlw(company)
    # print(type(cshFlw))
    # print(cshFlw)
    # print(cshFlw[0]['depreciationAndAmortization'])

    sharesOutstanding = get_entVal(company)
    price = get_price(company)

    # Calculate Remaining Inputs
    # * Tax Rate - tr
    # * Debt to Equity Ratio - de
    # * Normalize Net Income - normNetInc
    # * Normalized Net Capital Expenditures - normCapex
    # * Normalized Working Capital Change - normWCC
    # * Normalized Net Debt Issued - normDI
    # * Non-Cash ROE - nonCshRoe
    # * Equity Reinvestment Rate - eqReRate
    # * Levered Beta - beta
    # * Cost of Equity - coe
    # * Net Income Growth Rate - growthNI

    # Calculate effective tax rate
    tr = (incStmnt['incomeBeforeTax'] - incStmnt
          ['netIncome'][0]) / incStmnt['incomeBeforeTax']
    print(f'taxrate {tr}')

    # Calculate debt to equity ratio
    de = (balSht['totalLiabilities'][0]) / balSht['totalStockholdersEquity'][0]
    print(f'de {de}')

    # Calculate normalized net income
    totalNI = 0
    totalII = 0

    for x in range(len(incStmnt['netIncome'])):
        print(len(incStmnt['netIncome']))
        print(x)
        print(incStmnt['netIncome'][x])
        totalNI += incStmnt['netIncome'][x]
        print(incStmnt['interestIncome'][x])
        totalII = + incStmnt['interestIncome'][x]

    normNI = (totalNI - totalII)/len(incStmnt['netIncome'])
    print(f'Total NI {totalNI}')
    print(f'Total Int Inc {totalII}')
    print(f'normNI {normNI}')

    # Calculate normalized capital expenditures
    totalCapex = 0
    totalEbit = 0
    i = range(len(cshFlw['capex']))
    for x in i:
        totalCapex += ((cshFlw['capex'][x]*-1) - cshFlw['depreciation'][x])
        # print(f'Totcap {totalCapex}')
        totalEbit += incStmnt['ebit'][x]
        # print(f'TotEbit {totalEbit}')

    normCapex = (totalCapex / totalEbit) * incStmnt['ebit'][0]

    print(f'totalCapex {totalCapex}')
    print(f'ebit {totalEbit}')
    print('ebit 0 ' + str(incStmnt['ebit'][0]))
    print(f'normCapex {normCapex}')

    # Calculate normalized changes in working capital
    normWCC = ((balSht['totalCurrentAssets'][0] -
                balSht['cashAndCashEquivalents'][0] -
                balSht['totalCurrentLiabilities'][0])
               / incStmnt['totalRevenue'][0]) * (incStmnt['totalRevenue'][0] - incStmnt['totalRevenue'][1])
    print(f'WCC {normWCC}')

    # Calculate normalized debt issued
    normDI = balSht['totalLiabilities'][0] / \
        (balSht['totalLiabilities'][0] +
         balSht['totalStockholdersEquity'][0]) * (normCapex + normWCC)

    print('Liabilities ' + str(balSht['totalLiabilities'][0]))
    print('Equity ' + str(balSht['totalStockholdersEquity'][0]))
    print(f'Debt Issued {normDI}')

    # Calculate non cas return on equity
    nonCshRoe = normNI / \
        (balSht['totalStockholdersEquity'][1] -
         balSht['cashAndCashEquivalents'][1])

    print('Cash &' + str(balSht['cashAndCashEquivalents'][0]))
    print(f'ROE {nonCshRoe}')

    # Calculate equity reinvestment rate
    eqReRate = (normCapex + normWCC - normDI) / \
        (incStmnt['netIncome'][0] - incStmnt['interestIncome'][0])

    print('NI ' + str(incStmnt['netIncome'][0]))
    print('II ' + str(incStmnt['interestIncome'][0]))
    print(f'Rein Rate {eqReRate}')

    # Calculate beta
    beta = unleveredBeta * (1 + (1 - tr)) * de
    print(f'Beta {beta}')

    # Calculate cost of equity
    coe = riskFree + beta * EQPREM
    print(f'COE {coe}')

    # Calculate growth rate of net income
    growthNI = (nonCshRoe * eqReRate)
    print(f'Growth in Net Income {growthNI}')

    # Calculate wealth creation % if non cash roe > coe = wealth creation
    wealthCreate = nonCshRoe - coe
    print(f'Wealth creation {wealthCreate}')

    # Calculate present value of future free cash flows to equity
    totPvFcfe = 0
    expectedNI = []
    fcfe = []
    pvFcfe = []

    for year in range(growthPeriod):
        if year == 0:
            expectedNI.append(normNI * (1 + growthNI))
        else:
            expectedNI.append(expectedNI[year - 1] * (1 + growthNI))
        fcfe.append(expectedNI[year] * (1 - eqReRate))
        cumCoe = (1 + coe)**(year + 1)
        pvFcfe.append(fcfe[year] / cumCoe)
        totPvFcfe += pvFcfe[year]
        print(f'PV FCFE {year} {pvFcfe[year]}')

    print(f'Total PV FCFE {totPvFcfe}')

    # Calculate stable period coe
    stableCOE = riskFree + stableBeta * EQPREM

    # Calculate Terminal Value
    terminalValue = (expectedNI[-1] * (1 + stableGrowth)
                     * (1 - StableEqRe)) / (stableCOE - stableGrowth)

    print(f'PV Year 5 {pvFcfe[4]}')
    print(f'Terminal Value {terminalValue}')

    # Calculate Total PV of Operating Assets
    totalPvOpAssets = totPvFcfe + terminalValue

    print(f'PV of operating assets {totalPvOpAssets}')

    # Calculate Total PV of Equity in Firm
    totPvEq = totalPvOpAssets + balSht['cashAndCashEquivalents'][0]

    print(f'Total PV of Equity {totPvEq}')

    # Calculate Value per share
    pvEqPerShare = totPvEq / sharesOutstanding

    # Calculate the margin of safety (does the present value of the equity shares exceed the current price?)
    safetyMargin = pvEqPerShare - price

    print(f'Equity per share {pvEqPerShare}')
    print(f'Price {price}')
    print(f'Margin of Safety {safetyMargin}')


if __name__ == '__main__':
    main()
