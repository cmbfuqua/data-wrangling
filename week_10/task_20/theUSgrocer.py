#%%
from altair.vegalite.v4.api import layer
import pandas as pd 
import altair as alt 
import numpy as np
from datetime import datetime

from pandas_datareader.data import DataReader
#Build the library(dygraphs) plot that shows the Kroger (KR) 
# stock price performance over five years.
#%%

kroger = DataReader('KR','yahoo',datetime(2016,11,15),datetime(2021,11,15))
#%%
kroger['company'] = 'Kroger'
kroger['num_stocks'] = 0
kroger.loc[kroger.index > datetime(2019,4,4),'num_stocks'] = 418.41
kroger['profit'] = kroger.Close * kroger.num_stocks
#%%
kroger['date'] = kroger.index
#%%
kroger['x'] = kroger.date
kroger['y'] = kroger.Close.round(2)
source = kroger
# %%
nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['x'], empty='none')

# The basic line
line = alt.Chart(source).mark_line(interpolate='basis').encode(
    alt.X('x:T',title = 'Date'),#x='x:T',
    alt.Y('Close',title = 'Closing Price',axis = alt.Axis(format = '$'), scale = alt.Scale(zero = False))#y='y:Q'
)

# Transparent selectors across the chart. This is what tells us
# the x-value of the cursor
selectors = alt.Chart(source).mark_point().encode(
    x='x:T',
    opacity=alt.value(0),
).add_selection(
    nearest
)

# Draw points on the line, and highlight based on selection
points = line.mark_point().encode(
    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
)

# Draw text labels near the points, and highlight based on selection
text = line.mark_text(align='left', dx=5, dy=-20).encode(
    text=alt.condition(nearest, 'y:Q', alt.value(' '))
)

# Draw a rule at the location of the selection
rules = alt.Chart(source).mark_rule(color='gray').encode(
    x='x:T',
).transform_filter(
    nearest
)
scale = alt.selection_interval(bind = 'scales')
# Put the five layers into a chart and bind the data
chart = alt.layer(
    line, selectors, points, rules, text
).properties(
    width=600, height=300, title = 'Kroger Stock in the Last 5 Years',
).add_selection(scale)

chart.save('kroger_time.json')
# %%
#Imagine that you invested $10,000 in kroger about two years
# ago on April 5th. Make a graph with dygraph that shows performance 
# dyRebased() to $10,000.
growth = kroger.loc[kroger.date > datetime(2019,4,5)]
growth = growth[['x','Close','profit','company']]
growth['y'] = (growth.profit/1000).round(2)
alt.renderers.enable('html')

#%%
source = growth
nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['x'], empty='none')

# The basic line
line = alt.Chart(source).mark_line(interpolate='basis').encode(
    alt.X('x:T',title = 'Date'),#x='x:T',
    alt.Y('y',title = 'Profits ($1000)',axis = alt.Axis(format = '$'), scale = alt.Scale(zero = False))#y='y:Q'
)

# Transparent selectors across the chart. This is what tells us
# the x-value of the cursor
selectors = alt.Chart(source).mark_point().encode(
    x='x:T',
    opacity=alt.value(0),
).add_selection(
    nearest
)

# Draw points on the line, and highlight based on selection
points = line.mark_point().encode(
    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
)

# Draw text labels near the points, and highlight based on selection
text = line.mark_text(align='right', dx=-5, dy=-20).encode(
    text=alt.condition(nearest, 'y:Q', alt.value(' '))
)

# Draw a rule at the location of the selection
rules = alt.Chart(source).mark_rule(color='gray').encode(
    x='x:T',
).transform_filter(
    nearest
)
scale = alt.selection_interval(bind = 'scales')
# Put the five layers into a chart and bind the data
chart = alt.layer(
    line, selectors, points, rules, text
).properties(
    width=600, height=300, title = 'Personal Profits Since April 5th 2019d',
).add_selection(scale)

chart.save('profits_time.html', embed_options={'renderer':'svg'})
chart
#%%
#%%
#Annotate the graphic with a note of the reason at two or more time 
# points, or intervals, where the price had significant shifts.