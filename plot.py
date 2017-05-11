import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

housing_df = pd.read_csv('artists_05_new_housing_processed.csv')

def convert_money(value):
    return float(value[1:])

housing_df['value'] = housing_df['Valuation'].apply(convert_money)

housing_df = housing_df[housing_df['value'] < 1000000] #restrict to houses<2mil
#housing_df = housing_df[housing_df['biz_count'] < 50] #restrict to <50 groc. stores.

lt1e5 = housing_df[housing_df['value'] < 100000]
lt2e5 = housing_df[(housing_df['value'] >= 100000) & (housing_df['value']<200000)]
lt3e5 = housing_df[(housing_df['value'] >= 200000) & (housing_df['value']<300000)]

lt4e5 = housing_df[(housing_df['value'] >= 300000) & (housing_df['value']<400000)]

lt5e5 = housing_df[(housing_df['value'] >= 400000) & (housing_df['value']<500000)]

lt6e5 = housing_df[(housing_df['value'] >= 500000) & (housing_df['value']<600000)]

lt7e5 = housing_df[(housing_df['value'] >= 600000) & (housing_df['value']<700000)]

lt8e5 = housing_df[(housing_df['value'] >= 700000) & (housing_df['value']<800000)]

lt9e5 = housing_df[(housing_df['value'] >= 800000) & (housing_df['value']<900000)]

lt10e5 = housing_df[(housing_df['value'] >= 900000) & (housing_df['value']<1000000)]

mean_gro = [lt1e5['biz_count'].mean(), lt2e5['biz_count'].mean(), lt3e5['biz_count'].mean(), lt4e5['biz_count'].mean(), lt5e5['biz_count'].mean(), lt6e5['biz_count'].mean(), lt7e5['biz_count'].mean(), lt8e5['biz_count'].mean(), lt9e5['biz_count'].mean(), lt10e5['biz_count'].mean()]
vals = ['100k', '100k to 200k',  '200k to 300k', '300k to 400k', '400k to 500k', '500k to 600k', '600k to 700k', '700k to 800k', '800k to 900k', '900k to 1000k']

## ax = lt1e5.plot.scatter(x='biz_count', y='value', color='DarkBlue', label='price < $100000', marker='.')
## lt2e5.plot.scatter(x='biz_count', y='value', color='DarkGreen', label='price < $200000', ax=ax, marker='.')
## lt3e5.plot.scatter(x='biz_count', y='value', color='r', label='price < $300000', ax=ax, marker='.')
## lt4e5.plot.scatter(x='biz_count', y='value', color='y', label='price < $400000', ax=ax, marker='.')
## lt5e5.plot.scatter(x='biz_count', y='value', color='k', label='price < $500000', ax=ax, marker='.')
## lt6e5.plot.scatter(x='biz_count', y='value', color='c', label='price < $600000', ax=ax, marker='.')

## ax = lt135.plot.bar(x='biz_count', y='value', color='DarkBlue', label='price < $100000', marker='.')
#plt.scatter(housing_df['biz_count'], housing_df['value'], marker='.')
y_pos = np.arange(len(vals))

plt.barh(y_pos, mean_gro, align='center', alpha=0.5)
plt.yticks(y_pos, vals)
plt.xlabel('Avg no of independent artists within 0.5 miles')
plt.title('Avg no. of independent artists near new houses, org. by price')
plt.tight_layout()
plt.show()


