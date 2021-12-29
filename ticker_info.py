import yfinance as yf
import pandas as pd
import re
import json
import mysql.connector
from dataclasses import dataclass


@dataclass
class StockCandidates:
    ticker: str
    fcf_yield: float
    momentum_12: float

    def calc_yield(self, freeCashFlow, enterpriseValue):
        try:
            fcf_yield = freeCashFlow / enterpriseValue
        except TypeError:
            fcf_yield = 0
        except KeyError:
            print(symbol)
            fcf_yield = 0

        return fcf_yield

    def calc_momentum(self, price_now, price_12mon):
        try:
            momentum12 = price_now / price_12mon
        except KeyError:
            momentum12 = 0
        except TypeError:
            momentum12 = 0
        return momentum12


# companies = ['akba', 'akr', 'akro', 'akts', 'akus', 'albo', 'alco', 'ale', 'alec',
#              'alex', 'alg', 'algs', 'algt', 'allk', 'allo', 'alrm', 'alrs', 'alta', 'altg']
companies = ['gtn']
# co_dict = {}

for company in companies:
    ticker = yf.Ticker(company)

    info = ticker.info
    for k, v in sorted(info.items()):
        print(k, v)
#     history = ticker.history(period='1y')

#     symbol = re.search(r"\<([A-Za-z0-9_]+)\>", str(ticker)).group(1)
#     stock_candidate = StockCandidates(symbol, 0.0, 0.0)
#     try:
#         stock_candidate.fcf_yield = stock_candidate.calc_yield(
#             info['freeCashflow'], info['enterpriseValue'])
#     except KeyError:
#         print(symbol)
#         stock_candidate.fcf_yield = 0
#     except TypeError:
#         stock_candidate.fcf_yield = 0
#         print(symbol)
#     if stock_candidate.fcf_yield >= .0485:  # S&P 500 average FCF Yield = 4.85%
#         stock_candidate.momentum_12 = stock_candidate.calc_momentum(
#             history.iloc[-1, 3], history.iloc[0, 3])
#         if stock_candidate.momentum_12 > 1.0:  # 12 month closing price momentum is positive
#             co_dict[symbol] = {}
#             co_dict[symbol]['FCF Yield'] = stock_candidate.fcf_yield
#             co_dict[symbol]['12Momentum'] = stock_candidate.momentum_12
#         else:
#             continue
#             # print('Not a candidate - momentum')
#     else:
#         continue
#         # print('Not a candidate - FCF Yield')


# with open('candidates.txt', 'a') as stocks_file:
#     stocks_file.write(json.dumps(co_dict))

# print(co_dict)