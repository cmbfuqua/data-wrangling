#%%
import pandas as pd 
import numpy as np 
import altair as alt 
import datetime
from dateutil import tz
import pytz

data = pd.read_csv('https://byuistats.github.io/M335/data/carwash.csv')
#%%
# UTC to Local
#https://thispointer.com/convert-utc-datetime-string-to-local-time-in-python/
format = '%Y-%m-%dT%H:%M:%SZ'

data['time_new'] = data.time.apply(lambda x: datetime.datetime.strptime(x,format))
data['time'] = data.time.apply(lambda x: datetime.datetime.strptime(x,format))
data['time_new'] = data.time_new.apply(lambda x: x.replace(tzinfo = pytz.UTC))
#print('local time {}   original time {}\n\n'.format(data['time_new'][0],data.time[0]))

local_zone = tz.tzlocal()
data['time_new'] = data['time_new'].apply(lambda x: x.astimezone(local_zone))
#print('local time {}   original time {}\n\n'.format(data['time_new'][0],data.time[0]))
data['time_new'] = data['time_new'].apply(lambda x: x.strftime(format))
data['time_new'] = data['time_new'].apply(lambda x: datetime.datetime.strptime(x,format))

print('local time {}   original time {}'.format(data['time_new'][0],data.time[0]))
#%%
data = data.drop(columns='time')
# %%
data['hour'] = data.time_new.apply(lambda x: x.hour)
data['date'] = data.time_new.apply(lambda x: str(x.year) + '/' + str(x.month) + '/' + str(x.day))
# %%
df1_sum = data.groupby(['hour','date'],as_index=False).amount.sum()
# %%
rxe = pd.read_csv('rxe.csv')
rxe = rxe.drop(columns='Unnamed: 0')
# %%
format2 = '%Y-%m-%d %H:%M:%S'
rxe['dt'] = rxe.valid.apply(lambda x: datetime.datetime.strptime(x,format2))
rxe['hour'] = rxe.dt.apply(lambda x: x.hour)
rxe['date'] = rxe.dt.apply(lambda x: str(x.year) + '/' + str(x.month) + '/' + str(x.day))

# %%
rxe2 = rxe[['station','valid','dt','hour','date','tmpf']]

rxe_grouped = rxe2.groupby(['date','hour'],as_index=False).tmpf.mean()
# %%
from pandasql import sqldf
pysqldf = lambda q: sqldf(q, globals())

q = '''
select df1.date, df1.hour, amount,tmpf
from df1_sum df1
left join rxe_grouped df2 on df1.date = df2.date and df1.hour = df2.hour
'''
df_merge = pysqldf(q)
# %%
format3 = '%Y/%m/%d %H:%M:%S'
df_merge['date_time'] = df_merge.date + ' ' + df_merge.hour.astype(str) + ':00:00'
df_merge['date_time'] = df_merge.date_time.apply(lambda x: datetime.datetime.strptime(x,format3))
# %%
df_merge1 = df_merge.rename(columns={'amount':'sales','tmpf':'temp_F'})

data_chart = pd.melt(df_merge1,['date_time','date','hour'],['sales','temp_F']).sort_values(by = 'date_time')
# %%
scales = alt.selection_interval(bind = 'scales')
alt.Chart(data_chart, title = 'Temp vs Sales').mark_line().encode(
    alt.X('hour',title = 'Date and Hour'),
    alt.Y('mean(value)', title = None),
    alt.Color('variable')
).properties(
    width = 600
)
# %%
chart = alt.Chart(df_merge1).mark_point().encode(
    alt.X('hour',title = 'Hour',scale = alt.Scale(zero=False))
).properties(
    width = 400
)
chart.encode(alt.Y('temp_F', title = 'Temperature in Fahrenheit')).properties(title = 'Temperature Over Time')|chart.encode(alt.Y('sales', title = 'Sales')).properties(title = 'Sales Over Time')

# %%
alt.Chart(df_merge1).mark_point().encode(
    alt.X('sales'),
    alt.Y('temp_F')
)
# %%
alt.Chart()