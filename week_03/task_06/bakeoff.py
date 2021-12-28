#%%
import pandas as pd 
import altair as alt

data = pd.read_csv('ratings.csv')

#%%
data.columns
# %%
data.groupby('series').episode.min()
data.groupby('series').episode.max()
#%%
start = data.loc[data.episode == 1]
end = data.loc[
    ((data.episode == 6) & (data.series == 1)) |
    ((data.episode == 8) & (data.series == 2)) |
    ((data.episode == 10) & (data.series.isin([3,4,5,6,7,8,9,10])))
]


# %%
start.index = [x for x in range(len(start))]
end.index = start.index + 10

#%%

start['change_in_viewers'] = end.reset_index().viewers_7day - start.reset_index().viewers_7day
combined = pd.concat([start,end])

#%%
line = alt.Chart(combined, title = 'Change in viewers').mark_line(point = True).encode(
    alt.X('uk_airdate',title = 'Original Airdate in UK'),
    alt.Y('viewers_7day', title = 'Total Number of Viewers (MILLION)'),
    alt.Color('series:O',)
)
bar = alt.Chart(start).mark_bar().encode(
    alt.X('uk_airdate'),
    alt.Y('change_in_viewers'),
    alt.Color('series',legend = None)
)

line+bar
######################################################
# comparing the seasons for 10+
######################################################
# %%

ten = data.loc[(data.series.isin([3,4,5,6,7,8,9,10]))]

#%%
average7 = ten.groupby('series',as_index=False).viewers_7day.mean()
#%%
ten['series_mean'] = 0
for value in range(len(average7.series)):
    print(value)
    ten.loc[ten.series == average7['series'][value], 'series_mean'] = average7['viewers_7day'][value]

#%%
seven = alt.Chart(ten,title = 'Number of Viewers per Season').mark_line(point = True).encode(
    alt.X('uk_airdate',title = 'Date of the Episode'),
    alt.Y('viewers_7day',title = 'Number of Viewers (MIL)'),
    alt.Color('series')
)
seven

average = alt.Chart(ten,title = 'Number of Viewers per Season').mark_line().encode(
    alt.X('uk_airdate',title = 'Date of the Episode'),
    alt.Y('series_mean',title = 'Number of Viewers (MIL)'),
    alt.Color('series', title = 'Series')
)
average

alt.layer(seven,average).properties(width = 1200)




# %%
