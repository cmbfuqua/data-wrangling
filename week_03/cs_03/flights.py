#%%
import pandas as pd 
import altair as alt 
from nycflights13 import flights
alt.data_transformers.enable('default',max_rows = None)
flights.head()
#%%
#################################
# Question 1  For each origin airport (JFK, EWR, LGA), 
# which airline has the lowest 75th percentile of delay 
# time for flights scheduled to leave earlier than noon?
#################################
noon = flights.loc[flights.sched_dep_time <= 1200]
alt.Chart(noon, title = 'Distributions of Flights that Leave Before Noon').mark_boxplot().encode(
    alt.X('origin'),
    alt.Y('sched_dep_time', title = 'Time in HHMM or HMM')
)

#%%
#################################
# Question 2 Which origin airport is best to minimize my 
# chances of a late arrival when I am using Delta Airlines?
#################################
delta = flights.loc[flights.carrier == 'DL']

alt.Chart(delta,title = 'Distributions of Late Arrivals by Origin Airport').mark_point().encode(
    alt.X('origin', title = 'Origin Airport'),
    alt.Y('arr_delay',title = 'Arrival Delay in Minutes')
).configure_mark(
    opacity = .2
)



#%%
#################################
# Question 3 Which destination airport is the worst 
# (you decide on the metric for worst) for arrival delays?
#################################

worst = flights.loc[flights.arr_delay > 30]

alt.Chart(worst, title = 'The Worst Airports').mark_point().encode(
    alt.X('month', title = 'Month'),
    alt.Y('arr_delay', title = 'Arrival Delay'),
    alt.Column('origin', title = 'Origin Airport')
)

# %%
