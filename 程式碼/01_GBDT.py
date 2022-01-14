# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 21:07:01 2021

@author: Hsiao-Chiao Lin
"""

import pandas as pd

embedding = {'tfidf':'TFIDF_TruncatedSVD', 'w2v':'word2vec'}
source = ['covid','stock']
token = ['CKIP_nonEng', 'CKIPtoken', 'token']

embedding_choose = 'tfidf'
source_choose = source[0]
token_choose = token[1]

filename = '{}\{}_{}_stockSign_{}.csv'.format(embedding_choose,source_choose,token_choose, embedding[embedding_choose])
cvawname = 'cvaw\cvaw_{}_stockSign.csv'.format(source_choose)


data = pd.read_csv(filename)
cvaw = pd.read_csv(cvawname)

data = data.drop('Unnamed: 0', axis = 1)
cvaw = cvaw.drop('Unnamed: 0', axis = 1)

target, X_train, X_test, Y_train, Y_test = preprocess(data, cvaw)
GBDT_model(target, X_train, X_test, Y_train, Y_test)

print('\n',embedding_choose, source_choose, token_choose)

#%% preprocess

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

from sklearn.ensemble import GradientBoostingClassifier
from sklearn import metrics
import time

def GBDT_model(target, X_train, X_test, Y_train, Y_test, undersampling = 0):

    for i in range(0,3):
        
        y_column = target.columns[i]
    
        randomState = 404
        
        start = time.time()
        
        gb_model = GradientBoostingClassifier(n_estimators = 300, 
                                             subsample = 0.7,
                                            n_iter_no_change = 10,
                                             random_state = randomState)
        
        if undersampling == 1:
            X_train_under, Y_train_under = UnderSampling(X_train, Y_train[y_column])
            
            gb_model.fit(X_train_under, Y_train_under)
        
        else:
            gb_model.fit(X_train, Y_train[y_column])
            
        predicted_results = gb_model.predict(X_test)
        expected_results = Y_test[y_column]
        
        end = time.time()
        
        print("GBDT｜{}".format(y_column))
        print(metrics.classification_report(expected_results, predicted_results))
        print('mean score : {}'.format(round(gb_model.score(X_train, Y_train[y_column]), 2)))
        print("running time：%f sec" % (end - start))
        
#%% undersampling

from imblearn.under_sampling import RandomUnderSampler

def UnderSampling(X_train, Y_train):
    UnderSampler = RandomUnderSampler(random_state=404)
    X_train_under, Y_train_under = UnderSampler.fit_resample(X_train, Y_train)

    return X_train_under, Y_train_under


#%% parament

import numpy as np

learning_rates = np.arange(0.02, 0.1, 0.02)
min_samples_leafs = np.arange(50, 101, 25)

from sklearn.model_selection import GridSearchCV

parameters_to_search = {'learning_rate': learning_rates, 
              'min_samples_leaf': min_samples_leafs}

randomState = 99

y_column = target.columns[2]

gb_model = GradientBoostingClassifier(n_estimators = 300,
                                     subsample = 0.7,
                                    n_iter_no_change = 10,
                                     random_state = randomState)

gb_model_CV = GridSearchCV(gb_model, parameters_to_search, cv=5)
gb_model_CV.fit(X_train, Y_train[y_column])

gb_model_CV.cv_results_["mean_test_score"]
gb_model_CV.best_estimator_
