from datetime import datetime

x = datetime.today()
print(x.year)
print(x.month)
print(x.day)
print(type(x.day))
today = str(x.year) + str(x.month) + str(x.day)
print(today)

print(datetime.today())
