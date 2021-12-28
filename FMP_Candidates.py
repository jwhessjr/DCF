from numpy import NaN
import pandas as pd
from dataclasses import dataclass
import sqlite3
from sqlite3 import Error
import certifi
import json
from urllib.request import urlopen


@dataclass
class StockCandidates:
    ticker: str
    name: str
    sector: str
    industry: str
    fcf_yield: float
    momentum_12: float

    def calc_yield(self, freeCashFlow, marketCap):
        try:
            fcf_yield = freeCashFlow / marketCap
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
        except ZeroDivisionError:
            momentum12 = 0
        return momentum12


def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode('utf-8')
    return json.loads(data)
    return data


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

    for company in df['Ticker'][1501:]:

        url = ("https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey=83968f6306c788e28e55925ceabc45e1")
        co_list = get_jsonparsed_data(url)
        if company not in co_list:
            print(f'Company not in financial symbols list {company}')
            continue
        url = (
            f'https://financialmodelingprep.com/api/v3/ratios/{company}?apikey=83968f6306c788e28e55925ceabc45e1')
        ratios = get_jsonparsed_data(url)
        try:
            if ratios[0]['priceToFreeCashFlowsRatio'] == NaN or ratios[0]['priceToFreeCashFlowsRatio'] == None:
                print(ratios[0]['symbol'] + ' ' +
                      str(ratios[0]['priceToFreeCashFlowsRatio']))
                continue
        except IndexError:
            continue

        url = (
            f'https://financialmodelingprep.com/api/v3/profile/{company}?apikey=83968f6306c788e28e55925ceabc45e1')
        profile = get_jsonparsed_data(url)
        # if 'sector' not in profile[0]:
        #     print('No sector in profile' + profile[0]['symbol'])
        #     continue

        url = (
            f"https://financialmodelingprep.com/api/v3/historical-price-full/{company}?from=2020-12-01&to=2021-12-01&apikey=83968f6306c788e28e55925ceabc45e1")
        prices = get_jsonparsed_data(url)

        try:
            stock_candidate = StockCandidates(
                profile[0]['symbol'], profile[0]['companyName'], profile[0]['sector'], profile[0]['industry'], 0.0, 0.0)
        except IndexError:
            continue
        try:
            stock_candidate.fcf_yield = (
                1 / ratios[0]['priceToFreeCashFlowsRatio'])
        except ZeroDivisionError:
            stock_candidate.fcf_yield = 0
        if stock_candidate.fcf_yield >= .0485:  # S&P 500 average FCF Yield = 4.85%
            stock_candidate.momentum_12 = stock_candidate.calc_momentum(
                prices['historical'][-1]['close'], prices['historical'][0]['close'])
            if stock_candidate.momentum_12 > 1.0:  # 12 month closing price momentum is positive
                candidate = (stock_candidate.ticker, stock_candidate.name, stock_candidate.sector,
                             stock_candidate.industry, stock_candidate.fcf_yield, stock_candidate.momentum_12)
                print(candidate)
                candidate = create_candidate(conn, candidate)
            else:
                print('No MO' + '  ' + profile[0]['symbol'])
                continue

        else:
            continue

    print('Not a candidate - FCF Yield' + '  ' + profile[0]['symbol'])


# with open('candidates.txt', 'a') as stocks_file:
#     stocks_file.write(json.dumps(co_dict))
