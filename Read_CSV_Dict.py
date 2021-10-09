import pandas as pd

flDict = pd.read_csv('FLDCF20211006.csv', index_col=0,
                     header=None, squeeze=True).to_dict()

for key, value in flDict.items():
    print(key, value)
