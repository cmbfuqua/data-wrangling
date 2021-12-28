#%%
import pandas as pd 
import pyreadr
import pyreadstat
from simpledbf import Dbf5
from dbfread import DBF
#%%
us20 = pd.read_csv('https://raw.githubusercontent.com/hadley/r4ds/master/data/heights.csv')
print('read in csv')
#%%
b18 = pyreadstat.read_dta('germanconscr.dta')
#%%
b19 = pyreadstat.read_dta('germanprison.dta')
print('read in the dta files')
#g19 = Dbf5('B6090.DBF')
#g19 = dbf.to_dataframe()
g19 = pd.read_csv('my_dfb_file.csv')
print('read in the dbf files')
#%%
w20 = pd.read_spss('main05022005.sav')
print('read in the sav file')


# %%   select(birth_year, height.in, height.cm, study)
# Wrangle the csv df
us20['birth_year'] = '1950'
us20['study'] = 'us20'
#%%
us20 = us20[['birth_year','height','study']]
us20['height_cm'] = round(us20.height * 2.54,2)
#%% wrangle to b18 df
b18 = pd.DataFrame(b18)[0][0]
print(b18)
#%%
b18 = b18.rename(columns = {'bdec':'birth_year'})
#%%
b18['study'] = 'b18'
b18['height_in'] = b18.height * 0.393701

# %% Wrangle the b19 dataset
b19 = pd.DataFrame(b19)[0][0]
b19 = b19.rename(columns = {'bdec':'birth_year'})
#%%
b19['study'] = 'b19'
b19['height_in'] = b19.height * 0.393701

#%% Wrangle the g19 df
g19 = g19[['SJ','GEBJZ']]
g19 = g19.rename(columns = {'SJ':'birth_year','GEBJZ':'height'})
#%%
g19['study'] = 'g19'
g19['height_in'] = g19.height * 0.393701

#%%
w20 = w20[['DOBY','RT216F','RT216I']]
#%%
w20['height_in'] = (w20.RT216F * 12) + w20.RT216I
w20['study'] = 'w20'

#%% select(birth_year, height.in, height.cm, study)
us20 = us20[['birth_year','height','height_cm','study']]
us20 = us20.rename(columns = {'height':'height_in'})
#%%
b18 = b18[['birth_year','height_in','height','study']]
b18 = b18.rename(columns = {'height':'height_cm'})
#%%
b19 = b19[['birth_year','height_in','height','study']]
b19 = b19.rename(columns = {'height':'height_cm'})
#%%
g19 = g19[['birth_year','height_in','height','study']]
g19 = g19.rename(columns = {'height':'height_cm'})
#%%
w20['height_cm'] = w20.height_in * 2.54
w20 = w20[['DOBY','height_in','height_cm','study']]
w20 = w20.rename(columns = {'DOBY':'birth_year'})

#%%
w20.birth_year = w20.birth_year.astype(str)
w20.loc[w20.birth_year == 'REFUSED', 'birth_year'] = '0' 
#%%
w20.birth_year = w20.birth_year.astype(float) + 1900
#%%
w20.birth_year = w20.birth_year.astype(str).apply(lambda x: x[:-2])
# %%
final = pd.concat([us20,b19,b18,g19,w20],ignore_index=True)
# %%
import altair as alt
final1 = final.loc[final.height_in > 0]
final1 = final1.loc[final.height_in < 100]
alt.data_transformers.enable('default',max_rows = None)
chart = alt.Chart(final1, title = 'Height across the ages').mark_point().encode(
    alt.X('birth_year:T',title = 'Birth Year'),
    alt.Y('height_in', title = 'Height in Inches',scale = alt.Scale(zero = False)),
    alt.Facet('study',columns = 3),
)
chart
# %%
data = pd.read_csv('data_clean.csv')
rdata = pd.DataFrame([data,final])
#%%

pyreadr.write_rdata('final.RDS',final)
pyreadr.write_rdata('clean_table.RDS',data)
# %%
#data = [us20,b18,b19,g19,w20]

chart = alt.Chart(us20).mark_point().encode(
    alt.X('birth_year:T'),
    alt.Y('height_in')
)
chart
print('done')
