import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn import preprocessing

df=pd.read_csv('./ipl/all_matches.csv')

df1=df[['match_id','season','venue','innings','striker','bowler','batting_team','bowling_team','ball','runs_off_bat','extras']]
df1=df1[(df1.ball != 0.7) & (df.ball != 0.8) & (df.ball != 0.9) & (df.ball != 1.8) & (df.ball != 2.8) & (df.ball != 3.8) & (df.ball != 4.8)
        & (df.ball != 1.7) & (df.ball != 2.7) & (df.ball != 3.7) & (df.ball != 4.7)  & (df.ball != 2.9) & (df.ball != 1.9)& (df.ball != 3.9)
       & (df.ball != 4.9)]

df1=df1.loc[(df1['ball'] < 5.7) & (df1['innings']<3)]
df1['total'] = df1['runs_off_bat'] + df1['extras']
df2=df1.groupby(['match_id','innings'])[['total']].sum().reset_index()
list=df2['total']
list1=[]
for i in range(0,list.size,1):
    for j in range(0,36,1):
        list1.append(list[i])
df1['total_6']=list1[:58821]
df3=df1[['venue','season','ball','innings','striker','bowler','batting_team','bowling_team','total_6']]
team_encoding={'Mumbai Indians':1,
              'Royal Challengers Bangalore':2,
              'Kolkata Knight Riders':3,
              'Kings XI Punjab':4,
              'Chennai Super Kings':5,
              'Rajasthan Royals':6,
              'Delhi Daredevils':7,
              'Sunrisers Hyderabad':8,
              'Deccan Chargers':9,
              'Pune Warriors':10,
              'Delhi Capitals':11,
              'Gujarat Lions':12,
              'Rising Pune Supergiants':13,
              'Rising Pune Supergiant':13,
              'Kochi Tuskers Kerala':14}
team_encode_dict={'batting_team':team_encoding,
                 'bowling_team':team_encoding}
df3.replace(team_encode_dict,inplace=True)

ftr_list=['venue']
encoder=preprocessing.LabelEncoder()
for ftr in ftr_list:
    df3[ftr]=encoder.fit_transform(df3[ftr])
ftr_list1=['striker']
for ftr in ftr_list1:
    df3[ftr]=encoder.fit_transform(df3[ftr])
ftr_list2=['bowler']
for ftr in ftr_list2:
    df3[ftr]=encoder.fit_transform(df3[ftr])

X = df3[['venue','innings','batting_team','bowling_team','striker','bowler']]
y=df3['total_6'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=6)


regressor = RandomForestRegressor(n_estimators = 100, random_state = 4)
regressor.fit(X_train,y_train)
filename = 'first-innings-score-lr-model.pkl'
pickle.dump(regressor, open(filename, 'wb'))


