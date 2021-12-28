#%%
from altair.vegalite.v4.api import layer
import pandas as pd 
import altair as alt 
import numpy as np
from datetime import datetime

from pandas_datareader.data import DataReader
# %% Tesla HPI Apple
tesla = DataReader('TSLA','yahoo',datetime(2020,10,1),datetime(2021,11,14))
hpi = DataReader('HPI','yahoo',datetime(2020,10,1),datetime(2021,11,14))
apple = DataReader('AAPL','yahoo',datetime(2020,10,1),datetime(2021,11,14))
#%%
tesla['company'] = 'Tesla'
hpi['company'] = 'HPI'
apple['company'] = 'Apple'

tesla['investor'] = 'Friend'
hpi['investor'] = 'Friend'
apple['investor'] = 'Friend'

tesla['amt_invest'] = 500
hpi['amt_invest'] = 250
apple['amt_invest'] = 250

tesla['num_stocks'] = 1.115
hpi['num_stocks'] = 13.24
apple['num_stocks'] = 2.14

data1 = pd.concat([tesla,hpi,apple])

#%% Google HPE Amazon
google = DataReader('GOOGL','yahoo',datetime(2020,10,1),datetime(2021,11,14))
hpe = DataReader('HPE','yahoo',datetime(2020,10,1),datetime(2021,11,14))
amazon = DataReader('AMZN','yahoo',datetime(2020,10,1),datetime(2021,11,14))
#%%
google['company'] = 'Google'
hpe['company'] = 'HPE'
amazon['company'] = 'Amazon'

google['investor'] = 'Me'
hpe['investor'] = 'Me'
amazon['investor'] = 'Me'

google['amt_invest'] = 250
hpe['amt_invest'] = 250
amazon['amt_invest'] = 500

google['num_stocks'] = .17
hpe['num_stocks'] = 27.09
amazon['num_stocks'] = .155

data2 = pd.concat([google,hpe,amazon])
# %%
data = pd.concat([data1,data2])
data = data.drop(columns=['High','Low','Open','Volume','Adj Close'])

data['outcome'] = data.num_stocks * data.Close
data['date'] = data.index
# %%
me = data.loc[data.investor == 'Me']
friend = data.loc[data.investor == 'Friend']
me = alt.Chart(me, title = 'Investment Returns').mark_line(point = True).encode(
    alt.X('date', title = 'Date'),
    alt.Y('outcome', title = 'Price At Close x Number of Stocks'),
    alt.Color('company',title = 'Company',scale = alt.Scale(range=['orangered','red','darkred']))
)

friend = alt.Chart(friend, title = 'Investment Returns').mark_line(point = True).encode(
    alt.X('date', title = 'Date'),
    alt.Y('outcome', title = 'Price At Close x Number of Stocks'),
    alt.Color('company',title = 'Company',scale = alt.Scale(range=['steelblue','blue','darkblue']))
)

me|friend

#%%
alt.Chart(data, title = 'Investment Returns').mark_line(point = True).encode(
    alt.X('date', title = 'Date'),
    alt.Y('outcome', title = 'Price At Close x Number of Stocks'),
    alt.Color('company',title = 'Company'),
    alt.Facet('investor', title = 'Investor')
)

# %%
print(data.loc[data.date == data.date.max()].groupby(['investor','company'],as_index=False).outcome.sum()
.to_markdown())
print(data.loc[data.date == data.date.max()].groupby(['investor'],as_index=False).outcome.sum()
.to_markdown())
# %%
outcome_sum = data.groupby(['investor','date'],as_index=False).outcome.sum()
# %%
outcome_sum['outcomes'] = outcome_sum.outcome/100
alt.Chart(outcome_sum, title = 'Daily Sum of Stocks').mark_line().encode(
    alt.X('date',title = 'Date'),
    alt.Y('outcomes', title = 'Total profits ($100)', scale = alt.Scale(zero=False),axis = alt.Axis(format = '$')),
    alt.Color('investor',title = 'Investor')
)
# %%
