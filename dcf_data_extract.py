import yfinance as yf
import pandas as pd


balance_sheet = []
income_statement = []
cfs = []
risk_free_rate = []
beta = []
ten_year_rate = 0

company = ('gtn')


# summary = pd.DataFrame(columns=['Ticker', 'Net Income', 'Interest Income', 'Equity Book Value', 'Equity Book Value PY',
#                        'Cash & Securities', 'Cash & Securities PY', 'Equity Market Value', 'Shares Outstanding', 'CAPEX CY', 'Current Depreciation'])


# def get_data(ticker):
#     balance_sheet = yf.get_balance_sheet(ticker)
#     income_statement = yf.get_income_statement(ticker)
#     cfs = yf.get_cash_flow(ticker)
#     other_data = yf.get_stats(ticker)
#     years = balance_sheet.columns
#     data = (balance_sheet, income_statement, years)
#     return data


for symbol in company:
    try:
        ticker = yf.Ticker(symbol)
        # print(data)
        # print(type(data))

        balance_sheet = ticker.balance_sheet
        print(f'Balance Sheet {ticker} {balance_sheet}')
        print()
        print('------------------------------------------------')
        income_statement = ticker.financials
        print(f'Income Statement {ticker} {income_statement}')
        print()
        print('--------------------------------------------------')
        cfs = ticker.cashflow
        print(f'Cashflow {ticker} {cfs}')
        print()
        print()
    except:
        print(ticker + ': Something went wrong.')

#         print(income_statement[years[0]]['netIncome'])
#         print(balance_sheet[years[0]['totalStockholderEquity']])
#         # new_row = {'Ticker': ticker, 'Net Income': income_statement[years[0]]['netIncome'],
#         #            'Equity Book Value': balance_sheet[years[0]]['totalStockholerEquity']}
#         # summary = summary.append(new_row, ignore_index=True)
#         # print(ticker + ' added.')

# print(summary)
