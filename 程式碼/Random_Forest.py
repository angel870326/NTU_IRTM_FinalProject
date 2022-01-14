#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import classification_report


df_1 = pd.read_csv("cvaw_covid_stockSign.csv")
df_y = df_1.drop(['Unnamed: 0', "id", "date", "Valence_Sum", "Arousal_Sum", 'words_Num', 'Valence_Avg', 'Arousal_Avg'], axis=1)
df_y


# In[1]:


df2 = pd.read_csv("covid_token_stockSign_TFIDF_TruncatedSVD.csv")
df_x = df2.drop(['Unnamed: 0'], axis=1)
df_x


# In[103]:


df = pd.concat([df_x, df_y], axis=1)
df


# In[104]:


# 建立訓練與測試資料
X = df.drop(['stockRise_mask', 'stockRise_testKits', 'stockRise_vaccine'], axis=1) 
y1 = df['stockRise_mask']
X_train, X_test, y1_train, y1_test = train_test_split(X, y1, test_size=0.2, random_state=42)


# In[105]:


# 建立 random forest 模型
clf1 = RandomForestClassifier(n_estimators=500, max_features=50, random_state=404)
clf1.fit(X_train, y1_train)

# 預測
y1_test_predicted = clf1.predict(X_test)


# In[106]:


# 績效
cm1 = metrics.confusion_matrix(y1_test, y1_test_predicted)
print(cm1)
cl1 = classification_report(y1_test, y1_test_predicted)
print(cl1)
accuracy1 = accuracy_score(y1_test, y1_test_predicted)
print(accuracy1)
f1_1 = f1_score(y1_test, y1_test_predicted, average="micro")
print(f1_1)


# In[107]:


# 建立訓練與測試資料
y2 = df['stockRise_testKits']
X_train, X_test, y2_train, y2_test = train_test_split(X, y2, test_size=0.2, random_state=42)


# In[108]:


# 建立 random forest 模型
clf2 = RandomForestClassifier(n_estimators=500, max_features=50, random_state=404)
clf2.fit(X_train, y2_train)

# 預測
y2_test_predicted = clf2.predict(X_test)


# In[109]:


# 績效
cm2 = metrics.confusion_matrix(y2_test, y2_test_predicted)
print(cm2)
cl2 = classification_report(y2_test, y2_test_predicted)
print(cl2)
accuracy2 = accuracy_score(y2_test, y2_test_predicted)
print(accuracy1)
f1_2 = f1_score(y2_test, y2_test_predicted, average="micro")
print(f1_2)


# In[110]:


# 建立訓練與測試資料
y3 = df['stockRise_vaccine']
X_train, X_test, y3_train, y3_test = train_test_split(X, y3, test_size=0.2, random_state=42)


# In[111]:


# 建立 random forest 模型
clf3 = RandomForestClassifier(n_estimators=500, max_features=50, random_state=404)
clf3.fit(X_train, y3_train)

# 預測
y3_test_predicted = clf3.predict(X_test)


# In[112]:


# 績效
cm3 = metrics.confusion_matrix(y3_test, y3_test_predicted)
print(cm3)
cl3 = classification_report(y3_test, y3_test_predicted)
print(cl3)
accuracy3 = accuracy_score(y3_test, y3_test_predicted)
print(accuracy1)
f1_3 = f1_score(y3_test, y3_test_predicted, average="micro")
print(f1_3)


# In[ ]:




