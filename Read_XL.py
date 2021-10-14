import pandas as pd

file = "FLDCF20211006.xlsx"

inputs = pd.read_excel(file, sheet_name=0, index_col=0)

bal_sheet = pd.read_excel(file, sheet_name=1, index_col=0)
inc_stmnt = pd.read_excel(file, sheet_name=2, index_col=0)
cash_flow = pd.read_excel(file, sheet_name=3, index_col=0)

# print(inputs)
# print(bal_sheet)
# print(inc_stmnt)
# print(cash_flow)

dcf_inputs = pd.concat([inputs, bal_sheet, inc_stmnt, cash_flow])
# print(dcf_inputs)
# print(dcf_inputs.loc["Book Value of Equity", "Current Year"])
book_value = (dcf_inputs.at["Book Value of Equity", "Current Year"] +
              dcf_inputs.at["Book Value of Equity", "Prior Year"]) / 2

print(book_value)

# print(dcf_inputs.loc["Current Year"])
#print(dcf_inputs.loc["Book Value of Equity", "Current Year"])
#

# print(dcf_inputs.dtypes)
