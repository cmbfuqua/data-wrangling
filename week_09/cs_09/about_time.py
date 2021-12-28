#%%
import numpy as np 
import altair as alt 
import pandas as pd
import datetime 
import pytz

from dateutil import tz
from pandasql import sqldf
pysqldf = lambda q: sqldf(q, globals())

data = pd.read_csv('https://byuistats.github.io/M335/data/sales.csv')
# %%
data = data.rename(columns={'Name':'name','Type':'type','Time':'time','Amount':'amount'})
#%%
format = '%Y-%m-%dT%H:%M:%SZ'
data['time_new'] = data.time.apply(lambda x: datetime.datetime.strptime(x,format))
data['time_new'] = data.time_new.apply(lambda x: x.replace(tzinfo = pytz.UTC))
local_zone = tz.tzlocal()
data['time_new'] = data['time_new'].apply(lambda x: x.astimezone(local_zone))
data['time_new'] = data['time_new'].apply(lambda x: x.strftime(format))
#%%
data['time_new'] = data['time_new'].apply(lambda x: datetime.datetime.strptime(x,format))

data_d = data
#%%
data = data_d.loc[data.name != 'Missing']
#%%
data['hour'] = data.time_new.apply(lambda x: x.hour)
#############################################
# Done Preprocessing
#############################################

#%% Question 1 Provide an understanding and recommendation for hours of operation
# Question 2
data_1 = data.loc[data.amount <= 400]

#%%
alt.data_transformers.enable('default',max_rows = None)
chart1 = alt.Chart(data_1).mark_point().encode(
    alt.X('hour'),
    alt.Y('amount')
)

data_11 = data_1.loc[data_1.amount> 0]

alt.data_transformers.enable('default',max_rows = None)
chart2 = alt.Chart(data_1).mark_line().encode(
    alt.X('hour'),
    alt.Y('mean(amount)')
)
chart1 + chart2
#%%

data_11 = data_1.loc[data_1.amount> 0]

alt.data_transformers.enable('default',max_rows = None)
chart2 = alt.Chart(data_11).mark_line().encode(
    alt.X('hour'),
    alt.Y('count(amount)',title = 'Number of Customers')
)
chart2

#%%
# Question 3 
# Provide a final comparison of the six companies and a final recommendation.

chart1 = alt.Chart(data_1, title = 'Customers by Store').mark_point().encode(
    alt.X('hour'),
    alt.Y('amount', title = 'Number of Customers')
)

chart2 = alt.Chart(data_1, title = 'Customers by Store').mark_line().encode(
    alt.X('hour'),
    alt.Y('mean(amount)', title = 'Amount in Sales')
)
alt.layer(chart1,chart2).facet('name',columns=2)
#%%
chart1 = alt.Chart(data_1, title = 'Customers by Store').mark_line(point = True).encode(
    alt.X('hour'),
    alt.Y('count(amount)', title = 'Number of Customers'),
    alt.Color('name')
)

chart2 = alt.Chart(data_1, title = 'Customers by Store').mark_line().encode(
    alt.X('hour'),
    alt.Y('mean(count(amount))', title = 'Number of Customers')
)
chart1
#alt.layer(chart1,chart2).facet('name',columns=3)
# %%
from pandas_profiling import ProfileReport as pr 
pr(data)

