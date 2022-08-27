import pandas as pd
import numpy as np
import re

#generate separate csv files for each state
df=pd.read_csv('Age/07_01_Persons_arrested_by_sex_and_age_group_IPC_2012.csv')
dict1={}
for state in df['STATE/UT'].unique():
    dict1[state]={}
for state in dict1.keys():
    for index,row in df[df['STATE/UT']==state].iterrows():
        if not dict1[state].__contains__(row['CRIME HEAD']):
            dict1[state][row['CRIME HEAD']] = row[1:]
        else:
            dict1[state][row['CRIME HEAD']] += row[1:]
   # print(dict1[state])
    df1 = pd.DataFrame(dict1[state])
    df1 = df1.transpose()

   # print(df1.head(2))
    df1.to_csv('Age/' + state + '.csv')

#Remove female columns
for state in df['STATE/UT'].unique():
    temp = pd.read_csv('Age/' + state + '.csv')
    print(temp.columns)
    for i in temp.columns:
        x = re.search(".*Female.*", str(i))
        if (x):
            del temp[x.group(0)]
    del temp[temp.columns[0]]
    temp.to_csv('Age/' + state + '.csv',index=False)









