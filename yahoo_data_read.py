import yahoo_fin.stock_info as yf
import pandas as pd

balance_sheet = []
income_statement = []
cfs = []
years = []


summary = pd.DataFrame(
    columns=['Ticker', 'P/E', 'Profitability', 'Leverage', 'Operating Efficiency'])


tickers = ('fl', 'myrg', 'gtn', 'aapl')
# tickers = yf.tickers_dow()


def get_data(ticker):
    global balance_sheet
    global income_statement
    global cfs
    global years
    balance_sheet = yf.get_balance_sheet(ticker)
    income_statement = yf.get_income_statement(ticker)
    cfs = yf.get_cash_flow(ticker)
    pe_table = yf.get_quote_table(ticker)
    years = balance_sheet.columns


def pe(ticker):
    # global pe_ratio
    pe_ratio = pe_table['PE Ratio (TTM)']
    if pe_ratio != pe_ratio:  # Check for NaN
        pe_ratio = 0
    return pe_ratio


def profitability():
    # scores 1 -> net income (return on assets
    # if net income is > 0 then return on assets will be > 0 as well
    # global profitability_score
    net_income = income_statement[years[0]]['netIncome']
    net_income_py = income_statement[years[1]]['netIncome']
    ni_score = 1 if net_income > 0 else 0

    # score # 2 -> operating cash flow (op_cf_score)
    op_cf = cfs[years[0]]['totalCashFromOperatingActivities']
    op_cf_score = 1 if op_cf > 0 else 0

    # Score #3 -> change in return on assets (RoA_score)
    avg_assets = (balance_sheet[years[0]]['totalAssets']
                  + balance_sheet[years[1]]['totalAssets']) / 2
    avg_assets_py = (balance_sheet[years[1]]['totalAssets']
                     + balance_sheet[years[2]]['totalAssets']) / 2
    RoA = net_income / avg_assets
    RoA_py = net_income_py / avg_assets_py
    RoA_score = 1 if RoA > RoA_py else 0

    # Score #4 -> accruals (ac_score)
    total_assets = balance_sheet[years[0]]['totalAssets']
    accruals = op_cf / total_assets - RoA
    ac_score = 1 if accruals > 0 else 0

    profitability_score = ni_score + op_cf_score + RoA_score + ac_score
    return profitability_score


def leverage():
    # global leverage_score
    # Score #5 -> Long Term Debt Ratio
    try:
        lt_debt = balance_sheet[years[0]]['longTermDebt']
        total_assets = balance_sheet[years[0]]['totalAssets']
        debt_ratio = lt_debt / total_assets
        debt_ratio_score = 1 if debt_ratio <= .5 else 0
    except:
        debt_ratio_score = 1

     # Score #6 -> Current Ratio
    current_assets = balance_sheet[years[0]]['totalCurrentAssets']
    current_liab = balance_sheet[years[0]]['totalCurrentLiabilities']
    current_ratio = current_assets / current_liab
    current_ratio_score = 1 if current_ratio > 1 else 0

    # Score #7 -> Issueance of Stock
    # How to handle NaN in either field
    # net_new_shares = cfs[years[0]]['repurchaseOfStock'] + cfs[years[0]]['issuanceOfStock']
    # new_shares_score = 1 if net_new_shares <= 0 else 0

    leverage_score = debt_ratio_score + current_ratio_score
    return leverage_score


def operating_efficiency():
    # global operating_efficiency_score
    # Score #8 -> Gross Margin
    gp = income_statement[years[0]]['grossProfit']
    gp_py = income_statement[years[1]]['grossProfit']
    revenue = income_statement[years[0]]['totalRevenue']
    revenue_py = income_statement[years[1]]['totalRevenue']
    gm = gp / revenue
    gm_py = gp_py / revenue_py
    gm_score = 1 if gm > gm_py else 0

    # Score #9 -> Asset Turnover
    avg_assets = (balance_sheet[years[0]]['totalAssets']
                  + balance_sheet[years[1]]['totalAssets']) / 2
    avg_assets_py = (balance_sheet[years[1]]['totalAssets']
                     + balance_sheet[years[2]]['totalAssets']) / 2

    asset_turnover = revenue / avg_assets
    asset_turnover_py = revenue_py / avg_assets_py
    asset_turnover_score = 1 if asset_turnover > asset_turnover_py else 0

    operating_efficiency_score = gm_score + asset_turnover_score
    return operating_efficiency_score


for ticker in tickers:
    try:
        get_data(ticker)
        pe_ratio = pe(ticker)
        profitability_score = profitability()
        leverage_score = leverage()
        operating_efficiency_score = operating_efficiency()
        new_row = {'Ticker': ticker, 'P/E': pe_ratio, 'Profitability': profitability_score,
                   'Leverage': leverage_score, 'Operating Efficiency': operating_efficiency_score}
        summary = summary.append(new_row, ignore_index=True)
        print(ticker + ' added.')
    except:
        print(ticker + ': Something went wrong.')
summary['Total Score'] = summary['Profitability'] + \
    summary['Leverage'] + summary['Operating Efficiency']

print(summary)
