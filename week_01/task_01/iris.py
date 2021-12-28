#%%
import pandas as pd 
import altair as alt
from sklearn import datasets
iris = datasets.load_iris(as_frame=True)
                    #must put as_frame else returns a series without column headders
irisd = iris.data   #pulls out the data
irist = iris.target # pulls out the targets
irisf = iris.frame  # pulls out all of the data including the targets 
                    # So we can have the categories 0-2
irisn = iris.target_names#pulls out the names of the flowers
# %%
irisf['target_name'] = irisf.target.map({0:'setosa',1:'versicolor',2:'virginica'})
#add target names to iris frame
# %%
irisf.head()
#%%
irisf.describe()
# %%
chart = alt.Chart(irisf).mark_point().encode(
    alt.X('petal width (cm)',scale=alt.Scale(zero=False)),
    alt.Y('petal length (cm)',scale=alt.Scale(zero=False)),
    alt.Color('target_name')
)

chart + chart.transform_regression('petal width (cm)', 'petal length (cm)',groupby = ['target_name']).mark_line()
# %%
