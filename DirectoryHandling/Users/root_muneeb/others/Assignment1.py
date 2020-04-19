import csv
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Our Goal is to make a smalladataset based on only Games
from pandas import read_csv

# Read datafromcsv file
df = read_csv('laptops.csv')
# print(df.head(5));
# only finout the Category col
Category = df['Company']
# Print all the data
print(df)
# print only unique Categories
print(Category.unique());
# finot the apps in each cat
count = Category.value_counts()
# get all the rows from table where Category = Game
onlygames = df.loc[df['Company'] == 'Apple']
# save all the games data in new file
onlygames.to_csv('laptops.csv')
# get information about your data
onlygames.info()
print(df.head(5))
# x.scatter(x='Genre', y='Rating', data=onlygames, c='k', alpha=.15);
plt.scatter(x='Inches', y='Price_euros', data=df, c='k', alpha=.15);
# onlygames.hist(bins=5)
# onlygames['Price'].value_counts().plot(kind='bar')
# plt.scatter(onlygames['Price'], onlygames['Installs'])
# onlygames.plot()
plt.show()