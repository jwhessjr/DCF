import csv

with open('FLDCF20211006.csv', newline=") as dcfinputs:
    dcfvalues = csv.reader(dcfinputs, delimeter='', quotecharacter='|')
    for row in dcfvalues:
        print(','.join(row))
