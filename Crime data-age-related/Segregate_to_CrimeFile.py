import pandas
import pandas as pd

df=pd.read_csv('../TOTAL (ALL-INDIA).csv',index_col=[0])
print(df.head(2))
dict={}
df=df.transpose()
print(df.head(2))
for index,row in df.iterrows():
    dict[index]=row

#print(dict)


for i in dict.keys():
    dfD=pd.DataFrame(dict[i])
    dfD=dfD.iloc[:-2]
    dfD=dfD.assign(Low=[0,18,30,45,60])
    dfD=dfD.assign(Up=[18,30,45,60,100])
    print(dfD.head(10))
    dfD.to_csv('./'+i+'.csv',index=False)

for i in dict.keys():
    dfP=pd.read_csv('./'+i+'.csv')
    dfP.iloc[:,0]
    val=sum(dfP.iloc[:,0])
    li=[]
    for index,row in dfP.iterrows():
        value=row[i]
        li.append(value/val)

    dfP['Normalized']=li
    max1=max(dfP.iloc[:,0].to_list())
    ref=max1/5
    print(max1)
    li=[]
    for index,row in dfP.iterrows():
        value=row[i]
        if value>=4*ref:
            li.append(5)
        elif value>=3*ref:
            li.append(4)
        elif value>=2*ref:
            li.append(3)
        elif value>=ref:
            li.append(2)
        else:
            li.append(1)
    dfP['Points']=li

    dfP.to_csv('./'+i+'csv',index=False)

