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

# Calculate net income = net income - interest income
net_income = dcf_inputs.at["Net Income", "Current Year"] - \
    dcf_inputs.at["Interest Income", "Current Year"]

# print(net_income)
net_income = pd.Series(data=[net_income, " "],
                       index=dcf_inputs.columns, name="Adj Net Income")
dcf_inputs = dcf_inputs.append(net_income)
beta = 1.1
discount_rate = dcf_inputs["Risk Free Rate", "Current Year"] + \
    beta * dcf_inputs["Equity Risk Premium", "Current Year"]

discount_rate = pd.Series(
    data=[discount_rate, " "], index=dcf_inputs.columns, name="Discount_rate")
dcf_inputs = dcf-inputs.append(discount_rate)
print(dcf_inputs)
# print(book_value)

# print(dcf_inputs.loc["Current Year"])
#print(dcf_inputs.loc["Book Value of Equity", "Current Year"])
#

# print(dcf_inputs.dtypes)
