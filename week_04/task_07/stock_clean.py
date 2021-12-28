#%%
import pandas as pd 
import altair as alt
import pyreadr
#You are able to read in an .rds file in python, HOW COOL!
#%%
result = pyreadr.read_r('Dart_Expert_Dow_6month_anova.RDS')
#data = pd.read_csv('https://raw.githubusercontent.com/byuistats/data/master/Dart_Expert_Dow_6month_anova/Dart_Expert_Dow_6month_anova.csv')
data = result[None]
data.head()
# %% by DJIA
#data['year']= 0
data['year'] = data.contest_period.str.split('-',expand = True)[1].apply(lambda x: x[-4:])
data['month'] = data.contest_period.str.split('-',expand = True)[1].apply(lambda x: x[:-4])

data.loc[data.month == 'Febuary','month'] = 'February'
data.loc[data.month == 'Dec.', 'month'] = 'December'

#%%
data['month_num'] = data.month.map({'January':'1','February':'2','March':'3','April':'4','May':'5','June':'6','July':'7','August':'8','September':'9','October':'10','November':'11','December':'12'})

data['ym'] = data['month_num']+'/'+'01' + '/' +data['year']
print(data.ym)
data['ym'] = pd.to_datetime(data.ym,format="%m/%d/%Y")
print(data.ym)

#%%
# Create the plot

alt.Chart(data, title = 'Returns by 6 month period').mark_line().encode(
    alt.X('ym:T'),
    alt.Y('value:Q', title = 'Amount of returns'),
    alt.Color('variable',title = 'Deciding Group')
).properties(
    width = 1000
)



# %% use pd.pivot to get to the desired outcome
# you are supposed to use the DJIA form variable
test = data.loc[data.variable == 'DJIA']
#test = data.groupby(['month','year'],as_index=False).value.median()
#pivot the table so it matches the wide format
formated = test.pivot(index = 'month',columns = 'year',values = 'value')
# sort the columns so they are in order of months
test2 = formated
test2["index"] = pd.to_datetime(test2.index, format='%B', errors='coerce')
test2 = test2.sort_values(by="index")
test2 = test2.drop(columns = 'index')
# use this to round the numbers to 1 place
test3 = test2
for column in test3:
    test3[column] = test3[column].round(1)

test3.head(12)

# %%
pyreadr.write_rds('output.Rds',test3)
# %%
print(test3.to_markdown())