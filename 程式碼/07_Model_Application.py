# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 01:01:09 2021

@author: Hsiao-Chiao Lin
"""

#%% reading

import pandas as pd

embedding = {'tfidf':'TFIDF_TruncatedSVD', 'w2v':'word2vec'}
source = ['covid','stock']
token = ['CKIP_nonEng', 'CKIP', 'token']

embedding_choose = 'tfidf'
source_choose = source[0]
token_choose = token[1]

filename = '{}\{}_{}_stockSign_{}.csv'.format(embedding_choose,source_choose,token_choose, embedding[embedding_choose])
cvawname = 'cvaw\cvaw_{}_stockSign.csv'.format(source_choose)


data = pd.read_csv(filename)
cvaw = pd.read_csv(cvawname)

data = data.drop('Unnamed: 0', axis = 1)
cvaw = cvaw.drop('Unnamed: 0', axis = 1)

#%% model

from sklearn.ensemble import GradientBoostingClassifier

randomState = 404

select_model = GradientBoostingClassifier(n_estimators = 300, 
                                     subsample = 0.7,
                                    n_iter_no_change = 10,
                                     random_state = randomState)
        
#%% preprocessing

from sklearn.preprocessing import StandardScaler

emotion = cvaw[['Valence_Sum','Arousal_Sum','words_Num']]

scaler = StandardScaler().fit(emotion)
emotion = pd.DataFrame(scaler.transform(emotion), columns = ['Valence_Sum','Arousal_Sum','words_Num'])

data_df = pd.concat([data, emotion], axis = 1)

data_df = pd.concat([data, cvaw['date']], axis = 1)
data_df['month'] = data_df.date.str[:7]

data_df['y'] = cvaw['stockRise_vaccine']

#%% testing

import numpy as np
from sklearn.metrics import accuracy_score

month_list = list(data_df['month'].unique())

predict_output = {}
true_output = {}

guess, non_guess, correct = 0, 0, 0

doc_accu_list = []
month_doc_accu_list = []
day_accu_list = []
month_accu_list = []
predict_month = []

correct_answer = []

for index in range(0,len(month_list)-3):
    
    time_range = month_list[index:index+4]
    predict_month.append(time_range[3])
        
    y = 'y'
    x = list(data_df.columns[:-3])
    
    x_train = data_df[data_df['month'].isin(time_range[0:3])][x]
    y_train = data_df[data_df['month'].isin(time_range[0:3])][y]
    
    select_model.fit(x_train, y_train)
    
    test_date = list(data_df[data_df['month'] == time_range[3]]['date'].unique())
    
    predict_updown = {}
    true_updown = {}
    
    doc_accu = []
    day_accu = []
    
    for day in test_date:
        x_test = data_df[data_df['date'] == day][x]
        y_test = data_df[data_df['date'] == day][y]
        y_predict = select_model.predict(x_test)
        
        doc_accu.append(accuracy_score(y_test, y_predict))
        
        #vote = sum(y_predict)/len(y_predict)
        
        unique, counts = np.unique(y_predict, return_counts=True)
        counts = counts/counts.sum()
        votes = dict(zip(unique, counts))
          
        threshold = 0.9 ## setting
        
        for vote in votes:
            
            if votes[vote] >= threshold:
                predict_updown[day] = vote
                guess += 1
                
            else:
                predict_updown[day] = '-'
                non_guess += 1
        
        
        true_updown[day] = int(y_test.mean())
        
        if predict_updown[day] == true_updown[day]:
            correct += 1
            correct_answer.append(predict_updown[day])
            day_accu.append(1)
            
        else:
            day_accu.append(0)
            
        
        doc_accu_list.append(np.mean(doc_accu))
        day_accu_list.append(np.mean(day_accu))
    
    month_doc_accu_list.append(np.mean(doc_accu_list))
    month_accu_list.append(np.mean(day_accu_list))
        
    predict_output[time_range[3]] = predict_updown
    true_output[time_range[3]] = true_updown
    
    print("{} completed".format(time_range))


correct_rate = round(correct/guess,2)
guess_rate = round(guess/(guess+non_guess),2)


print('\n門檻值：{}'.format(threshold))
print("正確率：{}　辨別率：{}".format(correct_rate, guess_rate))

#%% plot

import matplotlib.pyplot as plt

plt.figure(figsize = (30,10))
plt.plot(predict_month,month_accu_list,'-o')
plt.grid(True)
plt.title("Monthly Prediction Accuracy", fontsize = 30)
plt.axhline(
    np.mean(month_accu_list),
    color='red',
    linestyle='dashed',
    linewidth=1
    )


plt.figure(figsize = (30,10))
plt.plot(predict_month,month_doc_accu_list,'-o')
plt.grid(True)
plt.title("Documents Prediction Accuracy", fontsize = 30)
plt.axhline(
    np.mean(month_doc_accu_list),
    color='red',
    linestyle='dashed',
    linewidth=1
    )