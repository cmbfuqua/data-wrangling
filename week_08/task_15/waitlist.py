#%%
import pandas as pd 
import altair as alt 
from datetime import datetime

data = pd.read_csv('waitlist_DP_108.csv')

#%%
data['Registration Date'] = data['Registration Date'].apply(lambda x: datetime.strptime(x, '%m/%d/%Y %H:%M'))

#%%
data18 = data.loc[data['Course Sec'] == 'FDMAT108-18']

students = data18.sort_values(by = ['Person ID','Registration Date','Status'],ascending = False)
waitlist = students.drop_duplicates(subset=['Person ID'])

registered = waitlist.loc[(waitlist.Status == 'Registered')].Status.count()
waitlistc = waitlist.loc[waitlist['Waitlist Reason'] == 'Waitlist Registered'].Status.count()
print(registered)
print(waitlist)
# %% filter to only include FDMAT108-18

def func1(data,course):
    data18 = data.loc[data['Course Sec'] == course]

    students = data18.sort_values(by = ['Person ID','Registration Date','Status'],ascending = False)
    waitlist = students.drop_duplicates(subset=['Person ID'])

    registered = waitlist.loc[(waitlist.Status == 'Registered')].Status.count()
    waitlistc = waitlist.loc[waitlist['Waitlist Reason'] == 'Waitlist Registered'].Status.count()
    print(waitlistc)
    print('/')
    print(registered)
    return waitlistc/registered
# %%
q1 = func1(data,'FDMAT108-18')
#
# %%
def func2(data,course):
    data18 = data.loc[data['Course Sec'] == course]

    students = data18.sort_values(by = ['Person ID','Registration Date','Status'],ascending = False)
    waitlist = students.drop_duplicates(subset=['Person ID'])

    waitlistc = waitlist.loc[waitlist['Waitlist Reason'] == 'Waitlist Registered'].Status.count()
    
    total_waitlist = data18.groupby('Status')['Person ID'].count()[2]
    print(waitlistc)
    print('/')
    print(total_waitlist)
    return waitlistc/total_waitlist
# %%
q2 = func2(data,'FDMAT108-18')
# %%
