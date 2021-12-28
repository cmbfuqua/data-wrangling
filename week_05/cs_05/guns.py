#%%
import pandas as pd 
import altair as alt 

data = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/guns-data/master/full_data.csv')
# %%
data['season'] = ''
data.loc[data.month.isin([12,1,2]),'season'] = 'winter'
data.loc[data.month.isin([6,7,8]),'season'] = 'summer'
data.loc[data.month.isin([3,4,5]),'season'] = 'spring'
data.loc[data.month.isin([9,10,11]),'season'] = 'fall'

#%%
alt.data_transformers.enable('default',max_rows = None)
alt.Chart(data,title = 'Intent of Gun Handlers').mark_bar().encode(
    alt.X('year:O', title = 'Year'),
    alt.Y('count(intent)', title = 'The Count of Intent'),
    alt.Color('intent')
)


#%%
alt.Chart(data, title = 'Male vs Female Suicide Rates').mark_point().encode(
    alt.X('sex', title = None),
    alt.Y('count(intent)', title = 'Number of deaths'),
    alt.Color('season'),
    alt.Column('intent')
)
# %%

alt.Chart(data, title = 'Intents by Season').mark_bar().encode(
    alt.X('season'),
    alt.Y('age', title = 'Total Count by Intent'),
    alt.Color('sex'),
    alt.Column('intent')
)
# %%
alt.Chart(data, title = '').mark_point().encode(
    alt.X('education', title = None),
    alt.Y('count(education)', title = 'Number of deaths'),
    alt.Color('season'),
    alt.Column('intent')
)