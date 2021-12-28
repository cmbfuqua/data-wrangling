# Homework Title
# Ben Fuqua
## "2021-09-23"
## class: "CSE 350 01"
## hours: .5 
## Palmer
----------------------------------------



```python
import pandas as pd 
from pandas_profiling import ProfileReport as pr 
import altair as alt 

```


```python
data = pd.read_csv('https://byuistats.github.io/M335/data/rcw.csv')
#change
```

# Question For RC&W attendance, what is the growth trend over time by department?


```python
alt.data_transformers.enable('default')
alt.Chart(data,title = 'Growth over time at RC&W Conference').mark_line().encode(
    alt.X('Semester_Date:T',title = 'Start date of the semester'),
    alt.Y('Count',title = 'Number of Attendees'),
    alt.Color('Department')
)

```




    
![png](output_4_0.png)
    



Chart that demonstrates the change over time  



