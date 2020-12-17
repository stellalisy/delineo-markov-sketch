import pandas as pd
import csv


# reader = csv.DictReader(open('Barnsdall_2020_03_02_full.csv'))

data = pd.read_csv('Barnsdall_2020_03_02_full.csv')
print(data.info())
print(len(data))

with open('Barnsdall_2020_03_02_full.csv') as data:
    reader = csv.DictReader(data)
    for row in reader:
        print(row)
