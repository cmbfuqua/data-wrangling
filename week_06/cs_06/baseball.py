# %%
import pandas as pd 
import altair as alt
import numpy as np
import sqlite3
import datadotworld as dw

#pip install dataDOTworld sqlite3
# LINK TO DATA https://data.world/byuidss/cse-250-baseball-database/workspace/dataset?agentid=byuidss&datasetid=cse-250-baseball-database
# This way of accessing the data has all of the same tables as the R package
# create a data.world account then import datadotworld as dw then run dw configure
# then go to your account -> setting -> advanced and grab the read/write api token and paste it into the console


# %% This connects us to the Lahman Database VIA the sqlite3 module
sqlite_file = 'lahmansbaseballdb.sqlite'
con = sqlite3.connect(sqlite_file)
sqlite_file = 'lahmansbaseballdb.sqlite'
con = sqlite3.connect(sqlite_file)
# See the tables in the database
table = pd.read_sql_query(
    "SELECT * FROM sqlite_master WHERE type='table'",
    con)

#print(table.filter(['name']))
# %%
# Use SQL to pull data from the DB

#get the people information
query = '''
SELECT *
FROM People
'''
# insert the table name next to 'FROM'
people = dw.query('byuidss/cse-250-baseball-database',query).dataframe

# get salary data
query = '''
SELECT *
FROM Salaries
'''
# insert the table name next to 'FROM'
salary = dw.query('byuidss/cse-250-baseball-database',query).dataframe

# get the school information
query = '''
SELECT *
FROM Schools
'''
# insert the table name next to 'FROM'
school = dw.query('byuidss/cse-250-baseball-database',query).dataframe

query = '''
SELECT *
FROM CollegePlaying
'''
# insert the table name next to 'FROM'
school_play = dw.query('byuidss/cse-250-baseball-database',query).dataframe


# %%
# run 'pip install cpi' to adjust for inflation
import cpi
salary['salary_2017'] = salary.apply(lambda x: round(cpi.inflate(x.salary,x.yearid,to = 2017),2), axis = 1)

#%%
school_u = school.loc[school.state =='UT']
table1 = people[['playerid','namefirst','namelast','namegiven']]
table2 = salary[['playerid','salary_2017','yearid','salary']]
table3 = school_u[['schoolid','name_full']] #
table4 = school_play[['playerid','schoolid']] #
#%%
from pandasql import sqldf
pysqldf = lambda q: sqldf(q, globals())

q = """
SELECT namefirst as fname, 
       namelast as lname,
       namegiven as name,
       salary_2017,
       name_full as school_name,
       yearid,
       salary
FROM table1 t1
JOIN table2 t2 on t1.playerid = t2.playerid
JOIN table4 t4 on t1.playerid = t4.playerid
JOIN table3 t3 on t3.schoolid = t4.schoolid
"""
# I didn't pass in a WHERE clause because I pre-filtered the data in the
# previous cell
data = pysqldf(q)

# %%
data['byu'] = 'Other'
data.loc[data.school_name == 'Brigham Young University','byu'] = 'BYU'
# %%
alt.Chart(data, title = 'BYU Baseball Salaries Compared To Other Utah Schools').mark_boxplot(size = 30).encode(
    alt.X('byu', title = None),
    alt.Y('salary_2017', title = 'Salaries of Players')
).properties(
    width = 200
)
# %%
byu_data = data.loc[data.byu == 'BYU']
other_data = data.loc[data.byu == 'Other']

byu = alt.Chart(byu_data).mark_line(strokeDash=[1,1]).encode(
    alt.X('yearid:O', title = 'Year'),
    alt.Y('mean(salary)', title = 'Average Salary'),
    alt.Color('name',title = None,legend = None,
              scale = alt.Scale(range = ['blue'])),
    
)
byu
#%%
other = alt.Chart(other_data,title = 'BYU(dashed) vs Other Utah Schools(solid)').mark_line().encode(
    alt.X('yearid:O', title = 'Year'),
    alt.Y('mean(salary)', title = 'Average Salary'),
    alt.Color('name',title = None,legend = None,
    scale = alt.Scale(range = ['orange']))
)
other
#%%
brandon = alt.Chart({'values':[{'x': 2008, 'y': 3500000}]}).mark_text(
    text='Brandon James', angle=295
).encode(
    x='x:O', y='y:Q'
)
Graph2 = brandon + other
#%%
Jeremy = alt.Chart({'values':[{'x': 2010, 'y': 5000000}]}).mark_text(
    text='Jeremy', angle=280
).encode(
    x='x:O', y='y:Q'
)
Brian = alt.Chart({'values':[{'x': 1999, 'y': 500000}]}).mark_text(
    text='Brian', angle=357
).encode(
    x='x:O', y='y:Q')
John = alt.Chart({'values':[{'x': 1991, 'y': 4500000}]}).mark_text(
    text='John Scott', angle=300
).encode(
    x='x:O', y='y:Q')
Wallace = alt.Chart({'values':[{'x': 1994, 'y': 5000000}]}).mark_text(
    text='Wallace Keith', angle=340
).encode(
    x='x:O', y='y:Q'
    )
Reid = alt.Chart({'values':[{'x': 1994, 'y': 3800000}]}).mark_text(
    text='Richard Warren', angle=300
).encode(
    x='x:O', y='y:Q'
    )
Other1 = alt.Chart({'values':[{'x': 1993, 'y': 1800000}]}).mark_text(
    text='James Cory', angle=0
).encode(
    x='x:O', y='y:Q'
    )
Other2 = alt.Chart({'values':[{'x': 1993, 'y': 500000}]}).mark_text(
    text='Vance Aaron', angle=0
).encode(
    x='x:O', y='y:Q'
    )
Other3 = alt.Chart({'values':[{'x': 1992, 'y': 300000}]}).mark_text(
    text='Wallace Reid', angle=0
).encode(
    x='x:O', y='y:Q'
    )
Graph1 = Jeremy+byu+Brian+John+Wallace+Reid+Other1+Other2+Other3
# %%
alt.layer(Graph1,Graph2).properties()
# %%
