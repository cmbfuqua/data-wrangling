#%%
import pandas as pd 
import altair as alt
alt.data_transformers.enable('default',max_rows = None)
from pyreadr import read_r
#%%
result = read_r('child_mortality.rda')
result.keys()
data = result['child_mortality']
# %% create the death to survival rate chart
base = alt.Chart(data, title = 'Survial To Deaths').encode(
    alt.X('year', scale = alt.Scale(zero = False), title = 'Year')
)

charta = base.mark_point(color = '#5276A7').encode(
    alt.Y('mean(survival_per_woman)', title = None)
)

chartb = base.mark_point(color = '#F18727').encode(
    alt.Y('mean(deaths_per_woman)', title = None)
)

alt.layer(charta,chartb).facet('continent',columns = 3).properties(
    title = ['Survival vs Deaths','Blue = Survival', 'Orange = Deaths']
)
# %% create the mortality rate to poverty
base = alt.Chart(data, title = 'Survial To Deaths').encode(
    alt.X('year', scale = alt.Scale(zero=False), title = 'Year')
)

charta = base.mark_point(color = '#5276A7').encode(
    alt.Y('mean(survival_per_woman)', title = None)
)
data['poverty_10'] = data.poverty/10
chartb = base.mark_bar(color = 'red').encode(
    alt.Y('mean(poverty_10)', title = None)
)

alt.layer(chartb,charta).facet('continent',columns = 3).properties(
    title = ['Survival vs Deaths','Blue = Survival', 'Red = Poverty']
)
# %%
