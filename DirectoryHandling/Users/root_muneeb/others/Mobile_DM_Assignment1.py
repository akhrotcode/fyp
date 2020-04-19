import csv
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# from pandas import read_csv
from pandas import DataFrame

data = pd.read_csv("googleplaystore.csv")
# df = DataFrame(data)
print(data.head(5))

df = pd.DataFrame(data)
print(df.corr())


x = data.Category
y = data.Installs
# plt.hist2d(x,y)
# plt.bar(x,y)
# plt.pie(x,y)
plt.scatter(x,y,label="Relation",c="maroon",s=40,marker="h",edgecolors="r",linewidths=1)
# plt.plot(x,y)

plt.show()
