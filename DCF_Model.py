#!/usr/bin/env python
# coding: utf-8

# # Valuation of an equity with 2 stage Discounted Cash Flow Model

# ## First acquire the inputs from the financial statements -
#     *  Balance Sheet
#     *. Income Statement
#     *. Cashflow Statement
#

# ## This model uses Yahoo Finance to acquire the financial statements

# ### Import the yfinance module to access Yahoo Finance

# In[1]:


from numpy import NaN
from dataclasses import dataclass
from sqlite3 import Error
import sqlite3
import re
import pandas as pd
import yfinance as yf

# ### Use yfinance to get the balance sheet for a equity using the stock ticker
#

# In[30]:


company = 'FL'
eq_prem = .0477
unlevered_beta = 1.03
risk_free = 0.0145
growth_period = 5
growth_stable = .02  # The CGR of the economy for the last 10 years.  Long term a company can't grow faster than the economy
eq_re_stable = .1333
coe_stable = .0622

# Get Info
try:
    ticker = yf.Ticker(company)
    info = ticker.info
except:
    print(ticker + ': Something went wrong')

# Get Balance Sheet
try:

    bs = ticker.balance_sheet

except:
    print(ticker + ': Something went wrong with BS')

bs_years = bs.columns

# Get Income Statement
try:
    ins = ticker.financials
except:
    print(ticker + ': Something went wrong with IS')

ins_years = ins.columns

# Get Cashflow Statement
try:
    cf = ticker.cashflow
except:
    print(ticker + ': Something went wrong CF')

cf_years = cf.columns


# In[31]:


print(re.search(r"\<([A-Za-z0-9_]+)\>", str(ticker)).group(1))
print(info)
print(bs)
print()
print(ins)
print()
print(cf)


# # Calculate inputs needed for DCF
#     * Interest Income from Cash & Marketable Securities (cy_int_inc)
#     * Tax Rate (tr)
#     * Debt to Equity Ratio (de)
#     * Sector Unlevered Beta (unleveled_beta) *input
#     * Risk Free Rate (risk_free) *input
#     * Equity Premium Rate (eq_prem) *input
#     * Normalized Net Income (ni)
#     * Normalized Net Capital Expenditures (CAPEX)
#     * Normalized Working Capital Change (WCC)
#     * Normalized Net Debt Issued (NDI)
#     * Non-Cash ROE (roe)
#     * Equity Reinvestment Rate (EQ_RE_Rate)
#     * Beta (beta)
#     * Cost of Equity (coe)
#     * Growth Rate in Net Income (growth-ni)

# In[4]:


if ins[ins_years[0]]['Interest Expense'] > 0:
    cy_int_inc = ins[ins_years[0]]['Interest Expense']
else:
    cy_int_inc = 0


# In[5]:


tr = (ins[ins_years[0]]['Income Before Tax'] - ins[ins_years[0]]
      ['Net Income']) / ins[ins_years[0]]['Income Before Tax']

print(f'Tax Rate {tr}')


# In[6]:


de = bs[bs_years[0]]['Total Liab'] / \
    info['marketCap']

print(f' D/E {de}')


# In[7]:


# Find source and automate (Aswath Damodaran website) - use the average unlevered beta for the sector


# In[8]:


# Find source and automate (Yahoo Finance has this)


# In[9]:


# Find source and automate (Aswath Damodaran website)


# In[10]:


normalized_ni = (ins[ins_years[0]]['Net Income'] + ins[ins_years[1]]['Net Income'] +
                 ins[ins_years[2]]['Net Income'] + ins[ins_years[3]]['Net Income']) / 4

print(f'Normalized NI {normalized_ni}')


# In[11]:


normalized_capex = (((cf[cf_years[0]]['Capital Expenditures'] + cf[cf_years[0]]['Depreciation']) + (cf[cf_years[1]]['Capital Expenditures'] + cf[cf_years[1]]['Depreciation']) + (cf[cf_years[2]]['Capital Expenditures'] + cf[cf_years[2]]['Depreciation']
                                                                                                                                                                                  ) + (cf[cf_years[3]]['Capital Expenditures'] + cf[cf_years[3]]['Depreciation']))) / ((ins[ins_years[0]]['Ebit'] + ins[ins_years[1]]['Ebit'] + ins[ins_years[2]]['Ebit'] + ins[ins_years[3]]['Ebit']) * ins[ins_years[0]]['Ebit']) * -1

print(f' Normalized CAPEX {normalized_capex}')


# In[12]:


normalized_wcc = ((bs[bs_years[0]]['Total Current Assets'] - bs[bs_years[0]]['Cash'] - bs[bs_years[0]]['Total Current Liabilities']
                   ) / ins[ins_years[0]]['Total Revenue']) * (ins[ins_years[0]]['Total Revenue'] - ins[ins_years[1]]['Total Revenue'])

print(f'Normalized WCC {normalized_wcc}')


# In[13]:


normalized_ndi = (bs[bs_years[0]]['Total Liab'] / (bs[bs_years[0]]['Total Liab'] +
                  bs[bs_years[0]]['Total Stockholder Equity'])) * (normalized_capex + normalized_wcc)

print(f'Normalized Debt Issued {normalized_ndi}')


# In[14]:


non_cash_roe = normalized_ni / \
    (bs[bs_years[1]]['Total Stockholder Equity'] - bs[bs_years[1]]['Cash'])

print(f'Non Cash ROE {non_cash_roe}')


# In[15]:


eq_re_rate = (normalized_capex + normalized_wcc - normalized_ndi) / \
    (ins[ins_years[0]]['Net Income'] - cy_int_inc)

print(f'Equity Reinvestment Rate {eq_re_rate}')
print(f'Currwnt Year Int Inc {cy_int_inc}')


# In[22]:


beta = unlevered_beta * (1 + (1 - tr)) * de

print(f'Levered Beta {beta}')


# In[17]:


coe = risk_free + (beta * eq_prem)

print(f'COE {coe}')


# In[18]:


growth_ni = non_cash_roe * eq_re_rate

print(f'Growth NI {growth_ni}')


# In[19]:


wealth_creation = non_cash_roe - coe

print(f'Wealth creation {wealth_creation}')


# # DCF Valuation

# In[28]:


# Present Value of free cash flow to equity for growth period
# in final version this will be an input

tot_pv_fcfe = 0
expected_ni = []
fcfe = []
pv_fcfe = []
for year in range(growth_period):
    if year == 0:
        expected_ni.append(normalized_ni * (1 + growth_ni))
    else:
        expected_ni.append(expected_ni[year-1] * (1 + growth_ni))

    fcfe.append(expected_ni[year] * (1 - eq_re_rate))
    cum_coe = (1 + coe)**(year + 1)
    pv_fcfe.append(fcfe[year] / cum_coe)
    tot_pv_fcfe += pv_fcfe[year]
    print(f' PV fcfe {year} {pv_fcfe[year]}')

print(f'Total PV FCFE {tot_pv_fcfe}')


# In[29]:


# Terminal Value Calculation


terminal_value = (pv_fcfe[growth_period - 1] * (1 + growth_stable)
                  * (1 - eq_re_stable)) / (coe_stable - growth_stable)

print(f'present value year 5 {pv_fcfe[4]}')
print(f' Terminal Value {terminal_value}')


# In[33]:


# Total PV of Operating Assets

total_pv_op_assets = tot_pv_fcfe + terminal_value

print(f'PV of Operating Assets {total_pv_op_assets}')


# In[34]:


# Total PV of the Equity in the Firm

total_pv_eq = total_pv_op_assets + bs[bs_years[0]]['Cash']

print(f'Total PV of Equity {total_pv_eq}')

pv_eq_pershare = total_pv_eq / info['sharesOutstanding']

print(f'PV per Share {pv_eq_pershare}')

current_price = info['currentPrice']
safety_margin = pv_eq_pershare - current_price
print(f'Current Price {current_price}')
print(f'Margin of Safety {safety_margin}')
