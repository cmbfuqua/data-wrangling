#%%
# Grab your city data from https://github.com/grammakov/USA-cities-and-states
import pandas as pd 
import altair as alt 
import re
from pandasql import sqldf
pysqldf = lambda q: sqldf(q, globals())


cities = pd.read_csv('us_cities.csv')

abc = pd.read_csv('abc7ny.csv')
kcra = pd.read_csv('kcra.csv')
# %%
abc['all_text'] = abc['headline'] + abc['teaser']
kcra['all_text'] = kcra['headline'] + kcra['teaser']

#%%
cities['city'] = cities.name.str.rsplit(' ',n=1,expand = True)[0]
cities_clean = pd.Series(cities.city.drop_duplicates())
# %%
city_long = ''
for place in cities_clean:
    city_long = city_long + '|' + place
city_long = city_long[1:]

# %%
abc['source'] = 'abc'
kcra['source'] = 'kcra'
data_full = pd.concat([kcra,abc],ignore_index=True).reset_index()
test = pd.DataFrame(data_full.all_text.apply(lambda x: re.findall(city_long,x)))

# %%
data_full['city'] = 'NO CITY'
for i,value in enumerate(test.all_text):
    if len(value) > 0:
        print(value,'  ',i)
        data_full['city'][i] = value[0]
    else:
        continue


# %%
top_15 = data_full.groupby('city',as_index=False).headline.count().sort_values(by = 'headline',ascending = False).head(16)[1:]

# %%
alt.Chart(top_15,title = 'Top 15 City Mentions').mark_bar().encode(
    alt.X('city',title = 'City',sort = '-y'),
    alt.Y('headline',title = 'Number of Occurances')
)
#%% Build the mentions over time graph for all of the top 15 cities
months15 = data_full.loc[data_full.city.isin(top_15.city)]
#%%
from datetime import datetime
months15['date'] = months15.datetime.str.rsplit(' ',n=2,expand = True)[0]
months15['month'] = months15.date.str.split(' ',expand = True)[0]
months15['year'] = months15.date.str.split(' ',expand = True)[2]
months15['date_'] = months15.year  +  '-'+ months15.month + '-' + '01'
months15 = months15.dropna(subset=['date_'])
#months15.date_ = pd.to_datetime(months15.date_, format = '%Y-%B-%d')
#%%
q = '''
select * 
from months15
'''
months151 = pysqldf(q)
test2 = months151.groupby(['date_','city'], as_index=False).index.count()
#%%
alt.Chart(test2).mark_line(point = True).encode(
    alt.X('date_:T', title = 'Date'),
    alt.Y('index',title = 'Number of Mentions'),
    alt.Color('city')
).properties(
    width = 400
)

# %%
small = data_full.loc[(data_full.city == 'Houston') | (data_full.city == 'Charlotte')]
#small2 = data_full.loc[data_full.city.isin(['Houston','Charlotte'])]

# %%
from datetime import datetime
small['date'] = small.datetime.str.rsplit(' ',n=2,expand = True)[0]
small['month'] = small.date.str.split(' ',expand = True)[0]
small['year'] = small.date.str.split(' ',expand = True)[2]
small['date_'] = small.month + '-' + '01' + '-' + small.year

#%%
q = '''
select * 
from small
where all_text not like '%Charlottesville%' 
'''
small2 = pysqldf(q)

#%%
test = small2.groupby(['date_','city'],as_index=False).index.count()
# %%
alt.Chart(test, title = 'Houston and Charlotte Headline Mentions').mark_line(point = True).encode(
    alt.X('date_:T', title = 'Year and Month'),
    alt.Y('index', title = 'Count of Headline Mentions'),
    alt.Color('city', title = 'City Name')
).properties(
    width = 300
)
# %%
