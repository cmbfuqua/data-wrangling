#%%
import pandas as pd 
import altair as alt 
from sklearn import datasets 

iris = datasets.load_iris(as_frame=True)
iris = iris.frame #This takes the data out of the iris set
iris['target_name'] = iris.target.map({0:'setosa',1:'versicolor',2:'virginica'})
# This maps the coded names into the actual names

#%%
# Let's create a plot to investigate relationship between Sepal.Width and Sepal.Length
# fill in the values below
chart = alt.Chart().mark_point().encode(
    alt.X(),
    alt.Y()
)
chart
#%%
# In the code below we encode the Species data with color, and make all the points diamond shape.
# Copy the code above and now map the color to species


#%%
#Notice that you can play with the scale of each aesthetic in a similar way. 
# Try changing the x and y axis to a log scale by adjusting the base argument.

chart = alt.Chart().mark_point().encode(
    alt.X('...', scale = alt.Scale(base = )),
    alt.Y('...', scale = alt.Scale(base = )),
    alt.Color()
)
chart

# %%
#Now, try to make setosa purple, versicolor orange and virginica blue
species = ['setosa', 'versicolor', 'virginica']
color = []

alt.Chart(iris).mark_point().encode(
    alt.X('petalWidth'),
    alt.Y('petalLength'),
    color=alt.Color('species', scale=alt.Scale(domain=species, range=color))
)

#%%
#You can get carried away with color. 
# Use the work many others have done for attractive, useful combinations.

alt.Chart(iris).mark_point().encode(
    alt.X('petalWidth'),
    alt.Y('petalLength'),
    alt.Color('species', scale=alt.Scale(scheme='dark2'))
)

#%%
#Fill in the blanks and the *** so that this code will run and so that the 
# labels will be placed in the right spot.

alt.Chart(iris, title = '******').mark_point().encode(
    alt.X('petalWidth', title = '*******'),
    alt.Y('petalLength', title = '******'),
    alt.Color('species', scale=alt.Scale(scheme='dark2'))
)

#%%
#How would you change the legend title to read "Species of Iris" instead?


alt.Chart(iris, title = '******').mark_point().encode(
    alt.X('petalWidth', title = '*******'),
    alt.Y('petalLength', title = '******'),
    alt.Color('species', ___ = alt._____(___ = ''))
)

#%%
#By adding `alt.Columns()` this code creates a separate panel (or columns) for each species, 
# instead of plotting them all on the same plot. 
alt.Chart(iris, title = '******').mark_point().encode(
    alt.X('petalWidth', title = '*******'),
    alt.Y('petalLength', title = '******'),
    alt.Color('species', ___ = alt._____(___ = '')),
    alt.Columns('*****')
)


