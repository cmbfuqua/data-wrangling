#%%
# Do pip install gapminder to access the data for this assignment
from altair.vegalite.v4.schema.core import Scale
from gapminder import gapminder as data
import pandas as pd 
import altair as alt


# %%
no_kuwait = data.loc[data['country'] != 'Kuwait']

#%%
no_kuwait['pop_reduced'] = no_kuwait['pop']/100000

# %%
continents = ['Africa','Americas','Asia','Europe','Oceania']
color_range = ['red','brown','green','blue','purple']
chart = alt.Chart(no_kuwait).mark_point().encode(
    alt.X('lifeExp', title = 'Life Expectancy',scale = alt.Scale(zero = False)),
    alt.Y('gdpPercap',title = 'GDP per capita'),
    alt.Size('pop_reduced',title = 'Population (100K)'),
    alt.Color('continent', scale = alt.Scale(domain = continents,range = color_range)),
    alt.Column('year',title = None)
    
).properties(
    width=100
)
chart
chart.save('life_expectancy.html')
# %%
