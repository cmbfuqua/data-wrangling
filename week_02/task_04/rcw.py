#%%
import pandas as pd 
import altair as alt 

data = pd.read_csv('https://byuistats.github.io/M335/data/rcw.csv')
#%%
alt.Chart(data,title = 'Growth over time at RC&W Conference').mark_line().encode(
    alt.X('Semester_Date:T',title = 'Start date of the semester'),
    alt.Y('Count',title = 'Number of Attendees'),
    alt.Color('Department')
)