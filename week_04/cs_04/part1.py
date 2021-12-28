#%%
import pandas as pd 
import altair as alt 

data = pd.read_excel('Height.xlsx',header = 2)
data.head()
# %%
#grab all of the columns that have data in them
data = data[['Code','Continent, Region, Country',1810,1820,1830,1840,1850,1860,1870,1880,1890,1900,1910,1920,1930,1940,1950,1960,1970,1980]]
# %%
data_filtered = data.dropna(how = 'all',subset = [1810,1820,1830,1840,1850,1860,1870,1880,1890,1900,1910,1920,1930,1940,1950,1960,1970,1980])
data_filtered = data_filtered.rename(columns = {'Continent, Region, Country':'Country'})
# %%
data_long = data_filtered.melt(id_vars = ['Code','Country'], value_vars = [1810,1820,1830,1840,1850,1860,1870,1880,1890,1900,1910,1920,1930,1940,1950,1960,1970,1980])
# %%
data_long = data_long.rename(columns = {'value':'height.cm','variable':'year_decade'})
# %%

data_clean = data_long.dropna(subset = ['height.cm'])
# %%
data_clean.year_decade = data_clean.year_decade.astype(str)
#%%
data_clean['century'] = data_clean.year_decade.apply(lambda x: x[:2])
data_clean['decade'] = data_clean.year_decade.apply(lambda x: x[2:3])
data_clean['year'] = data_clean.year_decade.apply(lambda x: x[-1:])
# %%
data_clean['height.in'] = data_clean['height.cm'].apply(lambda x: x * .3937008).round(5)
# %%Done cleaning the data
data_germany = data_clean.loc[data_clean.Country.isin(['Germany','Federal Republic of Germany (until 1990)'])]
data_ngermany = data_clean.loc[~data_clean.Country.isin(['Germany', 'Federal Republic of Germany (until 1990)'])]
#%% 
germany = alt.Chart(data_germany, title = 'Height over the decades').mark_point(color = 'black').encode(
    alt.X('year_decade:T'),
    alt.Y('height\.in:Q', scale = alt.Scale(zero = False))
)
ngermany = alt.Chart(data_ngermany, title = 'Height over the decades').mark_point(color = 'lightblue').encode(
    alt.X('year_decade:T'),
    alt.Y('height\.in:Q', scale = alt.Scale(zero = False))
)
ngermany + germany # the order here matters, the graphs stack from first to last
# because we want germany to be prevelant it must be on top. 
# %%
data_clean.to_csv('data_clean.csv')