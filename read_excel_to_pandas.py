import pandas as pd

df = pd.read_excel(
    '/Users/jhess/Library/Mobile Documents/com~apple~CloudDocs/dev/Python/DCF/russell_2000_symbols.xlsx')


for symbol in df['Ticker'][0:101]:
    print(symbol)
