# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 21:06:33 2021

@author: Hsiao-Chiao Lin
"""

import pandas as pd

embedding = {'tfidf':'TFIDF_TruncatedSVD', 'w2v':'word2vec'}
source = ['covid','stock']
token = ['CKIP_nonEng', 'CKIP', 'token']

embedding_choose = 'tfidf'
source_choose = source[1]
token_choose = token[2]

filename = '{}\{}_{}_stockSign_{}.csv'.format(embedding_choose,source_choose,token_choose, embedding[embedding_choose])
cvawname = 'cvaw\cvaw_{}_stockSign.csv'.format(source_choose)


data = pd.read_csv(filename)
cvaw = pd.read_csv(cvawname)

data = data.drop('Unnamed: 0', axis = 1)
cvaw = cvaw.drop('Unnamed: 0', axis = 1)

target, X_train, X_test, Y_train, Y_test = preprocess(data, cvaw)
NB_model(target, X_train, X_test, Y_train, Y_test,1)

print('\n',embedding_choose, source_choose, token_choose)

#%% preprocessing

def preprocess(data, cvaw):
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    
    emotion = cvaw[['Valence_Sum','Arousal_Sum','words_Num']]
    target = cvaw[['stockRise_mask', 'stockRise_testKits', 'stockRise_vaccine']]
    
    scaler = StandardScaler().fit(emotion)
    emotion = pd.DataFrame(scaler.transform(emotion), columns = ['Valence_Sum','Arousal_Sum','words_Num'])
    
    
    data = pd.concat([data, emotion], axis = 1)
    
    X_train, X_test, Y_train, Y_test = train_test_split(data, target, random_state=404, train_size=0.8)


    return (target, X_train, X_test, Y_train, Y_test)

#%% model

from sklearn.naive_bayes import GaussianNB
from sklearn import metrics


def NB_model(target, X_train, X_test, Y_train, Y_test, undersampling = 0):

    for i in range(0,3):
        y_column = target.columns[i]
        
        nb_model = GaussianNB()
        
        if undersampling == 1:
            X_train_under, Y_train_under = UnderSampling(X_train, Y_train[y_column])
            
            nb_model.fit(X_train_under, Y_train_under)
        
        else:
            nb_model.fit(X_train, Y_train[y_column])
            
        predicted_results = nb_model.predict(X_test)
        expected_results = Y_test[y_column]
        
        print("Gaussian NB | {}".format(y_column))
        print(metrics.classification_report(expected_results, predicted_results))
        #print('mean score : {}'.format(round(nb_model.score(X_train, Y_train[y_column]), 2)))
        

#%%
from imblearn.under_sampling import RandomUnderSampler

def UnderSampling(X_train, Y_train):
    UnderSampler = RandomUnderSampler(random_state=404)
    X_train_under, Y_train_under = UnderSampler.fit_resample(X_train, Y_train)

    return X_train_under, Y_train_under
