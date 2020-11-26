# -*- coding: utf-8 -*-
"""
Created on Sat May 18 15:20:21 2019

@author: gym
"""

import math
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import ensemble
from sklearn import datasets
from xgboost import XGBClassifier
import xgboost as xgb
from xgboost import plot_importance
from sklearn.model_selection import train_test_split
from sklearn import metrics
import xlwt

import pandas as pd
from sklearn import ensemble
from sklearn import datasets
from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error
from sklearn import metrics
import time
from sklearn import linear_model

from sklearn import linear_model
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn import metrics
from sklearn.preprocessing import MinMaxScaler,StandardScaler
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR,LinearSVR
from xgboost.sklearn import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn import ensemble
from sklearn.ensemble.forest import ExtraTreesRegressor
from sklearn.neighbors.regression import KNeighborsRegressor
from sklearn import metrics
#从数据库中读取训练数据
import pymysql
db=pymysql.connect(host="106.15.196.160",port=3306,user="root",password="root",db="zeolite")
cursor=db.cursor()
cursor.execute("SELECT * FROM zeolite.train_set")
data2=pd.DataFrame(list(cursor.fetchall()))
x=data2.iloc[:,1:4]
y=data2.iloc[:,4]


#load data
#data=pd.read_csv('1.csv')
#x_new=pd.read_csv('E:\zeolite\machine_learning\data_1911127\data_new2.csv')
#x=data.iloc[:,3:6]
#y=data.iloc[:,6]

#print(x)
#print(y)
#print(y)


#data cut
x_train,x_test,y_train,y_test=train_test_split(x,y,random_state=0,train_size=0.9)
#print(y_test)

#XGBoost

start=time.time()
model = xgb.XGBRegressor(max_depth=20,n_estimators=500,min_child_weight=8,subsample=0.9, colsample_bytree=0.9,reg_alpha=0, reg_lambda=0.5)
model.fit (x_train,y_train)
end=time.time()



#y_pred_train=model.predict(x_new)

#print(y_train)


#output data to excel


#y_pred_train_list=pd.DataFrame(y_pred_train)
#y_pred_train_list.to_excel('y_pred_train.xlsx')
#print(y_pred_train_list)
#Predict new data
#print(y_pred[1])
#print(model.predict(x_new))
#moredata=pd.DataFrame(model.predict(x_new))
#moredata.to_excel('moredata2.xlsx')

#save_pred(y_pred,'E:\zeolite\machine_learning\y_pred.xlsx')
#file.write(str(y_pred))
#file.close()









