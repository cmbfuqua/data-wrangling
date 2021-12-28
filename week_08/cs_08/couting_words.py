#%%
import pandas as pd 
import altair as alt
import numpy as np 
import re

from pyreadr import read_r

data = pd.read_csv('lds-scriptures.csv')
Savior = read_r('BoM_SaviorNames.rds')
savior = Savior[None]
# %%
bom = data.loc[data.volume_title == 'Book of Mormon'].reset_index()
# %%
text_long = ''
for index in range(len(bom)):
    text_long = text_long + ' ' + bom.scripture_text[index]
# %%
name_long = ''
for name in savior.name:    
    name_long = name_long + '|' + name
name_long = name_long[1:]  
# %%
text_split = re.split(name_long,text_long)
# %%
df = pd.DataFrame(text_split)
df = df.rename(columns={0:'split_text'})
df['split_length_nchar'] = df.split_text.apply(lambda x: len(x))
df['book'] = 'Book of Mormon'
df['split_length_word'] = df.split_text.apply(lambda x: len(x.split(' ')))
#%%
df['bin'] = ''
bins = ['0-10','11-20','21-30','31-40','41-50','51-60','61-70','71-80','81-90','91-100','100+']
df.loc[(df.split_length_word <= 10),'bin'] = bins[0]
df.loc[(df.split_length_word >= 11) & (df.split_length_word <= 20),'bin'] = bins[1]
df.loc[(df.split_length_word >= 21) & (df.split_length_word <= 30),'bin'] = bins[2]
df.loc[(df.split_length_word >= 31) & (df.split_length_word <= 40),'bin'] = bins[3]
df.loc[(df.split_length_word >= 41) & (df.split_length_word <= 50),'bin'] = bins[4]
df.loc[(df.split_length_word >= 51) & (df.split_length_word <= 60),'bin'] = bins[5]
df.loc[(df.split_length_word >= 61) & (df.split_length_word <= 70),'bin'] = bins[6]
df.loc[(df.split_length_word >= 71) & (df.split_length_word <= 80),'bin'] = bins[7]
df.loc[(df.split_length_word >= 81) & (df.split_length_word <= 90),'bin'] = bins[8]
df.loc[(df.split_length_word >= 91) & (df.split_length_word <= 100),'bin'] = bins[9]
df.loc[(df.split_length_word >= 101),'bin'] = bins[10]

# %%
alt.Chart(df, title = 'Length Between Mentions of Savior').mark_bar().encode(
    alt.X('bin', title = 'Length (Binned)',sort = '-y'),
    alt.Y('count(split_length_word)', title = 'Number of Occurances')
)

# %%
alt.Chart(df).mark_boxplot().encode(
    alt.X('book'),
    alt.Y('split_length_word')
)
# %% test how the split function works
string = 'the cow dog cow is cow jumping cows over cows the cows fence cows'
re.split('cows|cow|is',string)
# %%
