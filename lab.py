from numpy import NaN
import yfinance as yf
import pandas as pd
import re
from dataclasses import dataclass
import sqlite3
from sqlite3 import Error


@dataclass
class StockCandidates:
    ticker: str
    name: str
    sector: str
    industry: str
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


def create_connection(db_file):
    """ create a database connection to the companies database
    :parm db_file database file
    :return: Connection objesct or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_candidate(conn, candidate):
    """
    Create a new candidate into the candidates table
    :parm conn:
    :parm candidate
    :return: candidate ticker
    """

    sql = ''' INSERT INTO candidates(ticker, name, sector, industry, fcf_yield, momentum) VALUES(?, ?, ?, ?, ?, ?)'''

    cur = conn.cursor()
    cur.execute(sql, candidate)
    conn.commit()
    return cur.lastrowid


database = r'/Users/jhess/Library/Mobile Documents/com~apple~CloudDocs/dev/Python/DCF/companies.db'

df = pd.read_excel(
    '/Users/jhess/Library/Mobile Documents/com~apple~CloudDocs/dev/Python/DCF/russell_2000_symbols.xlsx')

conn = create_connection(database)
with conn:

    for company in df['Ticker'][901:1001]:
        ticker = yf.Ticker(company)
        info = ticker.info
        history = ticker.history(period='1y')
        symbol = re.search(r"\<([A-Za-z0-9_]+)\>", str(ticker)).group(1)

        if 'sector' not in info:
            continue
        if info['freeCashflow'] == NaN or info['freeCashflow'] == None:
            print(symbol + ' ' + str(info['freeCashflow']))
            continue
        stock_candidate = StockCandidates(
            symbol, info['longName'], info['sector'], info['industry'], 0.0, 0.0)
        stock_candidate.fcf_yield = stock_candidate.calc_yield(
            info['freeCashflow'], info['enterpriseValue'])
        if stock_candidate.fcf_yield >= .0485:  # S&P 500 average FCF Yield = 4.85%
            stock_candidate.momentum_12 = stock_candidate.calc_momentum(
                history.iloc[-1, 3], history.iloc[0, 3])
            if stock_candidate.momentum_12 > 1.0:  # 12 month closing price momentum is positive
                candidate = (stock_candidate.ticker, stock_candidate.name, stock_candidate.sector,
                             stock_candidate.industry, stock_candidate.fcf_yield, stock_candidate.momentum_12)
                print(candidate)
                candidate = create_candidate(conn, candidate)
            else:
                continue

        else:
            continue

    # print('Not a candidate - FCF Yield')


# with open('candidates.txt', 'a') as stocks_file:
#     stocks_file.write(json.dumps(co_dict))
