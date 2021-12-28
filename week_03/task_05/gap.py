#%%
# Do pip install gapminder to access the data for this assignment
from altair.vegalite.v4.schema.core import Scale
from gapminder import gapminder as data
import pandas as pd 
import altair as alt
import numpy as np


# %%#########################################################
# creating the weighted means graph
############################################################
no_kuwait = data.loc[data['country'] != 'Kuwait']
no_kuwait['pop_reduced'] = no_kuwait['pop']/100000
#%%
no_kuwait = no_kuwait.rename(columns = {'pop':'population'})

#%%
sum_of_weights = no_kuwait.groupby(['continent','year'],as_index = False).population.sum()
no_kuwait['multiplied_mean'] = no_kuwait.gdpPercap * no_kuwait.population
sum_of_values = no_kuwait.groupby(['continent','year'],as_index = False).multiplied_mean.sum()
data = sum_of_values
data['weighted_mean'] = data.multiplied_mean / sum_of_weights.population
#%%
no_kuwait['weighted_average'] = 0
for row in range(len(data)):
    no_kuwait.loc[(no_kuwait['continent'] == data['continent'][row]) & (no_kuwait['year'] == data['year'][row]),'weighted_average'] = data['weighted_mean'][row]
#%%

chart = alt.Chart().mark_line(point = True).encode(
    alt.X('year:O', title = 'Year'),
    alt.Y('gdpPercap',title = 'GDP per capita'),
    #alt.Size('pop_reduced',title = 'Population (100K)'),
    alt.Color('country', scale = alt.Scale(range = ['#aec7e8']), legend = None)
).properties(
    width=150
)

avg = alt.Chart().mark_line(point = True,color = 'black').encode(
    alt.X('year:O', title = 'Year'),
    alt.Y('weighted_average',title = 'GDP per capita')
).properties(
    width = 150
)


alt.layer(chart,avg,data = no_kuwait).facet(column = 'continent')

#%%
####################################################
# finding the greatest and smallest growth of each continent
#############################################################

start = no_kuwait.loc[no_kuwait['year'] == 1962]
end = no_kuwait.loc[no_kuwait['year'] == 2007]
end.index = start.index
start['end_lifeexp'] = end['lifeExp']
start['change_over_time'] = start['end_lifeexp'] - start['lifeExp'] 

# %%
sort_val = start.sort_values(by = ['continent','change_over_time'])

#%%
flitered = no_kuwait.loc[no_kuwait['country'].isin(['Zimbabwe','Libya','Trinidad and Tobago','Nicaragua','Iraq','Oman','Bulgaria','Turkey'])]


# %%
alt.Chart(flitered, title = 'Min and Max growth from each country').mark_line(point = True).encode(
    alt.X('year:O',title = 'Year'),
    alt.Y('lifeExp', title = 'Life Expectancy'),
    alt.Color('country', title = 'Name of Country'),
    alt.Column('continent', title = None)
)