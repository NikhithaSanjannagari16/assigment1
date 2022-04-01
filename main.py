import requests
import pandas as pd


url = 'https://datausa.io/api/data?drilldowns=State&measures=Population'


x = requests.get(url)
json_data = x.json()['data']
# json_data

df = pd.DataFrame(json_data)


years = df.Year.unique()[::-1]

states = df.State.unique()

def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(str(i))
    if n > 1:
        factors.append(str(n))
    return factors

csv_columns = ['State Name', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2019 Factors']

data = []
for state in states:
    row = []
    row.append(state)
    for year in years:
        curr_pop = df.loc[(df['Year'] == year) & (df['State'] == state)].values[0][4]
        if year == '2013':
            row.append(curr_pop)
        else:
            prev_pop = df.loc[(df['Year'] == str(int(year)-1)) & (df['State'] == state)].values[0][4]
            percentage = (curr_pop - prev_pop) * 100/ prev_pop
            per_string = '(' + str(round(percentage, 2)) + '% )'
            row.append(str(curr_pop) + per_string)
    prime_fs = prime_factors(df.loc[(df['Year'] == '2019') & (df['State'] == state)].values[0][4])
    prime_factors_str = ', '.join(prime_fs)
    row.append(prime_factors_str)

    data.append(row)

df = pd.DataFrame(data,columns=csv_columns)

df.to_csv('output.csv', index=False)