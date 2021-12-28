#%%
import pandas as pd 
import pyreadr
import pyreadstat

r = pyreadr.read_r('Dart_Expert_Dow_6month_anova.RDS')
r = r[None]
print('read in R')
csv = pd.read_csv('https://raw.githubusercontent.com/byuistats/data/master/Dart_Expert_Dow_6month_anova/Dart_Expert_Dow_6month_anova.csv')
print('read in CSV')
stat = pyreadstat.read_dta('Dart_Expert_Dow_6month_anova.dta')
stat = pd.DataFrame(stat[0]) # The [0] grabs the dictionary with all 
                             # the values
print('read in DTA')
sav = pd.read_spss('Dart_Expert_Dow_6month_anova.sav')
print('read in SAV')
xlsx = pd.read_excel('Dart_Expert_Dow_6month_anova.xlsx')
print('read in XLSX')
# %%
print(csv.equals(r))
print(csv.equals(stat))
print(csv.equals(sav))
print(csv.equals(xlsx))
# %%
import altair as alt 
import math
# working jitter chart
jitter = alt.Chart(csv, title = 'Values chart with Jitter').mark_point().encode(
    alt.X('jitter:Q', title=None,
        axis=alt.Axis(values=[0], ticks=True, grid=False, labels=False),
        scale=alt.Scale()),
    alt.Y('value', title = 'Amount of return'),
    alt.Color('variable', legend = None),
    alt.Column('variable:O',
        header=alt.Header(
            labelAngle=0,
            titleOrient='top',
            labelOrient='bottom',
            labelAlign='center',
            labelPadding=20))
).transform_calculate(
    jitter = 'sqrt(-2*log(random()))*cos(2*PI*random())'
).properties(
    width = 200
).configure_facet(
    spacing = 0
).configure_view(
    stroke = None
)
jitter
#%%
#working box plot
box = alt.Chart(csv, title = 'Values chart with Jitter').mark_boxplot().encode(
    alt.X('variable', title=None,
        axis=alt.Axis(values=[0], ticks=True, grid=False, labels=False),
        scale=alt.Scale()),
    alt.Y('value', title = 'Amount of return'),
    alt.Color('variable', legend = None)
).properties(
    width = 100
)
box
#%%
#putting them together
jitter = alt.Chart(csv).mark_point().encode(
    alt.X('jitter:Q', title = None,
          scale = alt.Scale(clamp = True),
          axis = None),
    alt.Y('value', title = 'Amount of return'),
    alt.Color('variable', legend = None)
).transform_calculate(
    jitter = 'sqrt(-2*log(random()))*cos(2*PI*random())'
)

box = alt.Chart(csv).mark_boxplot().encode(
    alt.Y('value', title = 'Amount of return'),
    alt.Color('variable', legend = None)
)

test = jitter+box
test.facet(column = 'variable', title = ''
).configure_title(
    anchor = 'middle'
)
#alt.layer(normal_chart,jitter_chart).facet(column = 'variable')
# %%
