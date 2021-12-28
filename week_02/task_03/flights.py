#%%
# must do 'pip install nycflights13' before you can run this script

# it is ok if it says it cannot resolved
from altair.vegalite.v4.schema.core import UrlData
from nycflights13 import flights

# flights is the combined, tidied data, but can also import individual pieces
# like this 'from nycflights13 import airports'

from pandas_profiling import ProfileReport as pr
# if you don't know what pandas_profiling is, google it. You're welcome :)

# %%
pr(f)

#%%
# In order for you to save charts in altair, you will first need to 
# install altair_saver, NodeJs from https://nodejs.org/en/download/ and click the 
# box that asks if you want it to install other necessary packages.
# Then run npm install vega-lite vega-cli canvas once it has finsihed installing
# then you can run 'name of your chart'.save('file_path')

# Normally this is what you would do, but as of 9/22/2021 the .pdf and .png formats
# don't work in altair due to an update. You can use the snipping tool to save it
# as a .png though
#%%
import altair as alt
alt.data_transformers.enable('default',max_rows = None)
#%%
alt.Chart(flights).mark_bar().encode(
    alt.X('origin'),
    alt.Y('count()')
)

#%%
alt.Chart(flights,title = 'Range of departure delays').mark_bar().encode(
    alt.X('dep_delay',bin = True, title = 'Departure Delays'),
    alt.Y('count()')
)
# %%
alt.Chart(flights,title = 'delays by origin').mark_bar().encode(
    alt.X('origin',title = 'Origin'),
    alt.Y('count(dep_delay)',title = 'Number of delayed departures')
)


#%%
