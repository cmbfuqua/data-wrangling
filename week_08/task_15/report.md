# Waitlist
# Ben Fuqua
## "2021-11-3"
## class: "CSE 350 01"
## hours: 2.5 
## Palmer
----------------------------------------
# Back Ground
Being waitlisted is never fun, it can be stressful and sometimes you need to get into this course otherwise you need to postpone your graduation! Here are some simple statistics on the waitlist for FDMAT108-18

### How many registered students in this section were on the waitlist?
```python
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
```
output = 21%

### Out of all of the students on the wait list, how many of them got into the course
```python
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

```

output = 20%