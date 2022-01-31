#!/usr/bin/env python
# coding: utf-8

# # DCF Model Using Financial Modeling Prep Inputs


# import required libraries

import pandas as pd
from urllib.request import urlopen
import sqlite3
from sqlite3 import Error
from datetime import datetime
import hg_dcflib




    cshFlw = hg_dcflib.get_cshFlw(company, myApiKey)

    entVal = hg_dcflib.get_entVal(company, myApiKey)
    sharesOutstanding = entVal[0]
    marketCap = entVal[1]

    price = hg_dcflib.get_price(company, myApiKey)

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
    # effective tr = (incStmnt['incomeTaxExpense'][0]/incStmnt['incomeBeforeTax'][0])
    # print(f'taxrate {tr}')
    tr = 0.21  # marginal tax rate of US firm

    # Calculate debt to equity ratio
    de = (balSht['totalLiabilities'][0]) / marketCap
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
        totalII += incStmnt['interestIncome'][x]

    normNI = (totalNI - totalII)/len(incStmnt['netIncome'])
    print(f'Total NI {totalNI}')
    print(f'Total Int Inc {totalII}')
    print(f'normNI {normNI}')

    # Calculate normalized capital expenditures
    # Adjust for R&D and acquisitions
    totalCapex = 0
    totalEbit = 0
    totalAcquisition = 0
    for x in range(len(cshFlw['capex'])):
        capex = (cshFlw['capex'][x]*-1)
        print(f"Capex {capex}")
        deprec = cshFlw['depreciation'][x]
        print(f"Depreciatiion {deprec}")
        acquisition = (cshFlw['acquisition'][x] * -1)
        print(f"Acquisitions {acquisition}")
        ebit = incStmnt['ebit'][x]
        print(f"Ebit {ebit}")
        totalCapex += (capex - deprec + acquisition)
        totalEbit += ebit

    normCapex = (totalCapex / totalEbit) * incStmnt['ebit'][0]

    print(f'totalCapex {totalCapex}')
    print(f'Total ebit {totalEbit}')
    print('ebit 0 ' + str(incStmnt['ebit'][0]))
    print(f'normCapex {normCapex}')

    # Calculate normalized changes in working capital
    # Adjust for short term debt (add it back)
    normWCC = (balSht['totalCurrentAssets'][0] -
               balSht['cashAndCashEquivalents'][0] -
               (balSht['totalCurrentLiabilities'][0] - balSht['shortTermDebt'][0]))\
        - (balSht['totalCurrentAssets'][1] -
           balSht['cashAndCashEquivalents'][1] -
           (balSht['totalCurrentLiabilities'][1] - balSht['shortTermDebt'][1]))
    print(f'normWCC {normWCC}')

    # Calculate normalized debt issued
    normDI = (balSht['totalLiabilities'][0] /
              (balSht['totalLiabilities'][0] +
               balSht['totalStockholdersEquity'][0])) * (normCapex + normWCC)

    print('Liabilities ' + str(balSht['totalLiabilities'][0]))
    print('Equity ' + str(balSht['totalStockholdersEquity'][0]))
    print(f'Debt Issued {normDI}')

    # Calculate non cas return on equity
    nonCshRoe = normNI / \
        (((balSht['totalStockholdersEquity'][0] -
         balSht['cashAndCashEquivalents'][0]) + (balSht['totalStockholdersEquity'][1] -
         balSht['cashAndCashEquivalents'][1])) / 2)

    print('Cash & ' + str(balSht['cashAndCashEquivalents'][0]))
    print(f'ROE {nonCshRoe}')

    # Calculate equity reinvestment rate
    eqReRate = (normCapex + normWCC - normDI) / \
        (incStmnt['netIncome'][0] - incStmnt['interestIncome'][0])

    print('NI ' + str(incStmnt['netIncome'][0]))
    print('II ' + str(incStmnt['interestIncome'][0]))
    print(f'Rein Rate {eqReRate}')

    # Calculate beta
    beta = unleveredBeta * (1 + (1 - tr) * de)
    print(f'Beta {beta}')

    # Calculate cost of equity
    print(f'risk free {riskFree}')
    print(f'beta {beta}')
    print(f'EQPREM {EQPREM}')
    coe = riskFree + (beta * EQPREM)
    print(f'COE {coe}')

    # Calculate growth rate of net income
    growthNI = (nonCshRoe * eqReRate)
    print(f'Growth in Net Income {growthNI}')

    # Calculate stable equity reinvestment
    stableEqRe = (STABLEGROWTH / growthNI) * eqReRate
    print(f'Stable Equity Reinvestment Rate {stableEqRe}')

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
    terminalValue = (expectedNI[-1] * (1 + STABLEGROWTH)
                     * (1 - stableEqRe)) / (stableCOE - STABLEGROWTH)

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
