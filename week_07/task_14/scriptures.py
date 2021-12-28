'''
Read in the .csv  file that was in the zip file and examine the structure of the data.
A numerical summary to address questions one and two using R functions from install.packages("stringr")  and install.packages("stringi") is sufficient.
Create a visualization that addresses question 3.
Create an .Rmd  file with one to two paragraphs and your graphics that answers the three questions.
Compile your .md  and .html  file into your git repository.
'''

'''Questions:
What is the average verse length (number of words) in the New Testament compared to the Book of Mormon?
How often is the word Jesus used in the New Testament compared to the Book of Mormon?
How does the word count distribution by verse look for each book in the Book of Mormon?
'''

#%%
import pandas as pd 
import altair as alt
import re

data = pd.read_csv('lds-scriptures.csv')
# %%
# Question 1: What is the average verse length in the new testament
# compared to the book of mormon?
new = data.loc[data.volume_title == 'New Testament']
new = new[['volume_title','book_title','chapter_number','verse_number','scripture_text']]
book = data.loc[data.volume_title == 'Book of Mormon']
book = book[['volume_title','book_title','chapter_number','verse_number','scripture_text']]
# %%
new['verse_count'] = new.scripture_text.str.split(' ',expand = True).count(axis = 1)
book['verse_count'] = book.scripture_text.str.split(' ',expand = True).count(axis = 1)
# %%
final = pd.concat([new,book])
# %%
print((final.groupby('volume_title').verse_count.mean().round(2)).to_markdown())
# %% How often is the word Jesus used in the New Testament compared to the Book of Mormon?
final['jesus_str'] = final.scripture_text.apply(lambda x: re.findall('(Jesus)',x))
# %%
print((final.groupby('volume_title').jesus_str.count()).to_markdown())
# %%How does the word count distribution by verse look for each book in the Book of Mormon?
books = ['1 Nephi','2 Nephi','Jacob','Enos','Jarom','Omni','Words of Mormon','Mosiah','Alma','Helaman','3 Nephi','4 Nephi','Mormon','Ether','Moroni']
alt.data_transformers.enable('default',max_rows = None)
alt.Chart(book, title = 'Word Count Distribution By Book ').mark_boxplot().encode(
    alt.X('book_title',title = 'Book Name',sort = books),
    alt.Y('verse_count', title = 'Words In Verse')
)
# %%
