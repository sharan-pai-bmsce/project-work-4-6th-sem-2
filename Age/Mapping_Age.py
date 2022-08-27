import pandas as pd
l = {
    'as': 'Assault',
    'ac': 'Accident',
    'tf': 'Traffic Law',
    'ht': 'Human Trafficking',
    'ar': 'Arson',
    'd': 'Drugs',
    'mi': 'Missing',
    'mu': 'Murder',
    'p': 'Public Nuisance',
    't': 'Theft',
    'r': 'Robbery',
    'g': 'Gun Violence',
    's': 'Sex Crime',
    'f': 'Fraud',
    'o': 'Others',
    'h': 'Harrassment',
    'cc': 'Child Crime',
}

temp={
    'ARSON (SECTION 435, 436, 438 IPC)' : l['ar'],
    'ASSAULT ON WOMEN WITH INTENT TO OUTRAGE HER MODESTY(SECTION 354 IPC)' : l['h'],
    'ATTEMPT TO COMMIT MURDER (SECTION 307 IPC)': l['mu'],
    'AUTO THEFT': l['t'],
    'BURGLARY (SECTION 449 TO 452, 454, 455, 457 TO 460 IPC)': l['r'],
    'CAUSING DEATH BY NEGLIGENCE (SECTION 304-A IPC)': l['ac'],
    'CHEATING (SECTION 419 TO 420 IPC)': l['f'],
    'COUNTERFEITING (SECTION 231-254 AND 489A TO 489D IPC)': l['f'],
    'CRIMINAL BREACH OF TRUST (SECTION 406 TO 409)': l['f'],
    'CRUELTY BY HUSBAND OR HIS RELATIVES (SECTION 498A IPC)': l['h'],
    'CULPABLE HOMICIDE NOT AMOUNTING MURDER (SECTION 304, 308 IPC)': l['mu'],
    'CUSTODIAL RAPE': l['s'],
    'DACOITY (SECTION  395 TO 398 IPC)': l['r'],
    'DOWRY DEATHS (SECTION 304B IPC)': l['mu'],
    'HURT (SECTION 323, 324 TO 333, 335 TO 338 IPC)': l['g'],
    'IMPORTATION OF GIRLS FROM FOREIGN COUNTRY(SECTION 366B IPC)': l['ht'],
    'INSULT TO THE MODESTY OF WOMEN(SECTION 509 IPC)': l['h'],
    'KIDNAPPING AND ABDUCTION (SECTION 363 TO 369, 371 TO 373 IPC)': l['mi'],
    'KIDNAPPING AND ABDUCTION OF OTHERS': l['mi'],
    'KIDNAPPING AND ABDUCTION OF WOMEN AND GIRLS': l['mi'],
    'MURDER (SECTION 302 IPC)': l['mu'],
    'OTHER RAPE': l['s'],
    'OTHER THEFT': l['t'],
    'PREPARATION AND ASSEMBLY FOR DACOITY (SECTION 399 TO 402 IPC)': l['r'],
    'RAPE (SECTION 376 IPC)': l['s'],
    'RIOTS (SECTION 143, 144, 145, 147, 148, 149, 150, 151, 153, 153A, 153B, 157, 158, 160 IPC)': l['p'],
    'ROBBERY (SECTION 392 TO 394, 397, 398 IPC)': l['r'],
    'THEFT (SECTION 379 TO 382 IPC)': l['t'],
    'OTHER IPC CRIMES': l['o'],
}

x=None
df=pd.read_csv('./07_01_Persons_arrested_by_sex_and_age_group_IPC_2012.csv')
for state in df['STATE/UT'].unique():
    temp2=pd.read_csv('./'+state+'.csv',index_col=[0])
    print(temp2.head(2))
    temp2=temp2.transpose()
    #temp2=temp2.iloc[1:,:]
    dict1={}
    for col in temp2.columns[1:len(temp2.columns)-1]:
        if temp[col] not in dict1:
            dict1[temp[col]]=0
        dict1[temp[col]]+=temp2[col]

    dfD=pd.DataFrame(dict1)
    dfD['total']=temp2['TOTAL COGNIZABLE IPC CRIMES']
    #df1.insert(0,'DISTRICT',temp2.iloc[:,0])
    print(dfD.head(10))
    dfD.to_csv('./'+state+'.csv')