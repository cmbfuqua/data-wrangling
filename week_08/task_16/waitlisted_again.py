#%%
import pandas as pd 
import altair as alt 
from datetime import datetime

data = pd.read_csv('../task_15/waitlist_DP_108.csv')

#%%
data['Registration Date'] = data['Registration Date'].apply(lambda x: datetime.strptime(x, '%m/%d/%Y %H:%M'))

# %% filter to only include FDMAT108-18

def func1(data,course):
    data18 = data.loc[data['Course Sec'] == course]

    students = data18.sort_values(by = ['Person ID','Registration Date','Status'],ascending = False)
    waitlist = students.drop_duplicates(subset=['Person ID'])

    registered = waitlist.loc[(waitlist.Status == 'Registered')].Status.count()
    waitlistc = waitlist.loc[waitlist['Waitlist Reason'] == 'Waitlist Registered'].Status.count()
    return waitlistc/registered

def func2(data,course):
    data18 = data.loc[data['Course Sec'] == course]

    students = data18.sort_values(by = ['Person ID','Registration Date','Status'],ascending = False)
    waitlist = students.drop_duplicates(subset=['Person ID'])

    waitlistc = waitlist.loc[waitlist['Waitlist Reason'] == 'Waitlist Registered'].Status.count()
    
    temp = data18.groupby('Status',as_index = False)['Person ID'].count()
    total_waitlist = temp.loc[temp.Status == 'Wait List'].reset_index()
    total_waitlist = total_waitlist['Person ID'][0]
    return waitlistc/total_waitlist
# %%
new_data = pd.DataFrame(columns=['semester','course_sec','waitlist_in_class','waitlist_to_class'])
for i,course in enumerate(data['Course Sec'].drop_duplicates()):
    wait = func1(data,course)
    overall = func2(data,course)
    sem = data.loc[data['Course Sec'] == course].reset_index()['Semester Term Code'][0]
    dic = {'semester':sem,'course_sec':course,'waitlist_in_class':wait,'waitlist_to_class':overall}
    new_data = new_data.append(dic,ignore_index=True)
new_data.head(10)

# %%
new_data2 = pd.melt(new_data,value_vars=['waitlist_in_class','waitlist_to_class'],id_vars=['semester','course_sec'])

# %%
alt.Chart(new_data2, title = 'Wait List Stats').mark_bar().encode(
    alt.X('semester:O'),
    alt.Y('value:Q'),
    alt.Column('variable:N')
)
# %%
alt.Chart(new_data2, title = 'Wait List Stats').mark_bar().encode(
    alt.X('variable:O'),
    alt.Y('value:Q'),
    alt.Column('semester:N')
)
# %%
print(new_data.sort_values(by='semester').to_markdown())
#%%
new_data2['value_percent'] = new_data2.value * 100
# %%
alt.Chart(new_data2).mark_line(point = True).encode(
    alt.X('semester'),
    alt.Y('mean(value)', title = '',axis = alt.Axis(format = '%')),
    alt.Color('variable', title = 'Waitlist type')
).properties(
    width = 200
)
# %%
