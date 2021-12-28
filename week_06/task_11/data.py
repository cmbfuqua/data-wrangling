#%%
import pandas as pd 
import altair as alt 

data = pd.read_csv('../../Data/attacks_proj.csv')
# %%
 
data = data.dropna(how = 'all',subset= ['Date','Country','Area','Location','Activity','Name','Age','Injury'])
data = data.drop(columns = ['Investigator or Source','pdf','href formula','href','Case Number.1','Case Number.2','original order','Unnamed: 22','Unnamed: 23'])
#%%
from pandas_profiling import ProfileReport as pr 
pr(data)
# %%
