#%%
import pandas as pd 
import altair as alt 
import re 
import sys
import urllib


url = "https://byuistats.github.io/M335/data/randomletters.txt"
file = urllib.request.urlopen(url)
let = ''
for line in file:
	decoded_line = line.decode("utf-8")
	let = let + decoded_line


url = ('https://byuistats.github.io/M335/data/randomletters_wnumbers.txt')
file = urllib.request.urlopen(url)
numlet = ''
for line in file:
	decoded_line = line.decode("utf-8")
	numlet = numlet + decoded_line
# %%With the randomletters.txt file, pull out every 1700 letter 
# (for example, 1, 1700, 3400, …) and find the quote that is hidden—
# the quote ends with a period.
quote = ''
for skip in range(0,len(let),1700):
    if skip == 0:
        quote = quote + let[skip]
    else:
        if let[skip-1] == '.':
            quote = quote + let[skip-1]
            break
        else:
            quote = quote + let[skip-1]
print(quote)

######
# OUTPUT: the plural of anecdote is not data.
######

# %% With the randomletters_wnumbers.txt file, find all the numbers hidden, 
# and convert those numbers to letters using the letters order in 
# the alphabet to decipher the message.

numbers = re.findall('\d+',numlet)
alphabet = {'0':'a','1':'b','2':'c','3':'d','4':'e','5':'f',
            '6':'g','7':'h','8':'i','9':'j','10':'k',
            '11':'l','12':'m','13':'n','14':'o','15':'p'
            ,'16':'q','17':'r','18':'s','19':'t','20':'u',
            '21':'v','22':'w','23':'x','24':'y','25':'z'}
phrase = []
for number in numbers:
    number = int(number)-1
    number = str(number)
    phrase.append(alphabet[number])
for letter in phrase:
    print(letter,end = '')

#######
# OUTPUT: experts often possess more data than judgment
#######

# %% With the randomletters.txt file, remove all the spaces and periods 
# from the string then find the longest sequence of vowels.

removed = re.findall('\w',let)


pat = ''
for remove in removed:
    pat = pat+remove

groups = re.findall('([aeiou]+)',pat)

print(len(max(groups, key=len)))

#######
# OUTPUT: 7
#######
# %%
