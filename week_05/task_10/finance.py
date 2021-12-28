#%%
import pandas as pd 
import altair as alt 
from pyreadr import read_r
from pandas_profiling import ProfileReport
#%%
result = read_r('financing_healthcare.rda')
# %%
data = result['financing_healthcare']
# %%
ProfileReport(data)
#%% number of rows 36873
filtered = data.drop(columns = ['health_insurance','nhs_exp','health_exp_private','health_insurance_govt',
'health_insurance_private','health_insurance_any','no_health_insurance'])
# %%
filtered['child_mort_'] = filtered.child_mort / 10
alt.data_transformers.enable('default',max_rows = None)
mortality = alt.Chart(filtered, title = 'Life Expectancy Compared to Child Mortality').mark_line().encode(
    alt.X('year', title = 'Year'),
    alt.Y('mean(child_mort_)', title = 'Child Mortality per 10,000 born'),
    alt.Color('continent')
)
# %%
life = alt.Chart(filtered, title = ' Life Expectancy Compared to Child Mortality').mark_line().encode(
    alt.X('year', title = 'Year'),
    alt.Y('mean(life_expectancy)', title = 'Life Expectancy'),
    alt.Color('continent')
)

#%%

alt.layer(mortality,life).resolve_axis(y = 'independent')
# %%
