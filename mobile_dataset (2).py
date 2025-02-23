# -*- coding: utf-8 -*-
"""Mobile_DataSet.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xr4W-03INeemENNE7wrowqePz1U1bcNK

# Machine Learning Project - Predicting Flipcart Sales Prices

## Import Libraries
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from statistics import mean
import seaborn as sns
from sklearn.metrics import accuracy_score,r2_score,mean_absolute_error,mean_squared_error,confusion_matrix,classification_report

"""## Store the CSV File"""

df=pd.read_csv("/content/Flipkart_Mobiles.csv");
df.head()

df['Brand']=df['Brand'].str.strip();
df['Model']=df['Model'].str.strip();

print(df.describe());

"""## Finding the type and No.of Null and Non-Null values in all columns"""

df.info()

"""## Finding the Number of rows and columns"""

print(df.shape);

"""## Finding the Number of NULL Values of each column"""

print(df.isna().sum());

"""## Drop the NULL Values"""

df1=df.copy(deep=True);
df1.dropna(inplace=True);
print(df1.isna().sum())

"""##Finding the duplicate Values"""

df1.duplicated().sum()

"""## Drop the duplicate values"""

df1.drop_duplicates(inplace=True);
print(df1.duplicated().sum());

"""## Findig the No.of NULL and Non-NULL values in all columns"""

df1.info();
print(df1["Memory"].value_counts());

df.hist(figsize=(14,7));

"""## Converting the Categorical into Numerical using LabelEncoder() Method"""

#dummy=pd.get_dummies(data=df1,columns=['Brand','Model','Color','Memory','Storage']);
from sklearn.preprocessing import LabelEncoder
df2=df1.copy(deep=True);
label_encoders = {}
for column in ['Brand', 'Model','Memory','Storage']:
    encoder = LabelEncoder()
    df2[column + '_encoded'] = encoder.fit_transform(df2[column])
    label_encoders[column] = encoder
print(df.head())

df2.head(10)

df2.iloc[:,5:].head()

a=df2.iloc[:,5:].corr()
a

"""## Plot the Bar Graph of Models between Original and Selling Prices"""

df2.loc[df2.Brand_encoded==5]

##df3=df1.iloc[:,:].copy(deep=True)
##df2["Brand"]=le.inverse_transform(df2["Brand"]);
name='SAMSUNG'
ram='4 GB'
import matplotlib.pyplot as plt
df3=df2.loc[df1['Brand']==name].copy(deep=True)
df3=df3[['Brand','Model','Memory','Original Price','Selling Price']]
##df3=df3.iloc[:,:].copy(deep=True)
print(df3.head())
col=['Brand','Model']
df3.drop_duplicates(subset=['Brand','Model','Memory'],inplace=True)
df3.loc[df3['Memory']==ram].plot(kind='bar',x='Model',y=['Original Price','Selling Price'])
plt.xlabel('Model')
plt.ylabel('Price')
plt.title(name+'-'+ram)
plt.figure(figsize=(50,50))
plt.show()

"""## Find the Dependent and Independent Variables"""

x=df2[['Brand_encoded','Model_encoded','Memory_encoded','Storage_encoded','Rating','Original Price']];
y=df2['Selling Price'];

x.head(10)

"""## Data Splitting"""

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=3)

"""## Model Building

### 1.Linear Regression Model
"""

from sklearn.linear_model import LinearRegression
slr=LinearRegression()

"""#### Fit the x_train,y_train in the Model"""

slr.fit(x_train,y_train);

"""#### Predicting the y_test"""

y_predi=slr.predict(x_test)

"""#### Finding the r2_score,accuracy_score,Root Mean Squared Error,Mean Absolute Error"""

from sklearn.metrics import accuracy_score,mean_squared_error,mean_absolute_error,r2_score
r2=r2_score(y_test,y_predi)
print(y_test.shape)
print(y_predi.shape)
#print(slr.score(y_test,y_predi))
root_mean_square=np.sqrt(mean_squared_error(y_test,y_predi))
mean_absolute=mean_absolute_error(y_test,y_predi)
print("Linear Regression Algorithm")
print("r2 score : ",r2)
print("Root Mean Squared Error :",root_mean_square)
print("Mean Absolute Error :",mean_absolute)

"""#### Predicting the Model"""

s_p=slr.predict([[11,125,19,3,4.5,17990]])
print("Selling Price :",s_p)

brand=df2.iloc[:,0].copy(deep=True)
print("List of Brands :",list(brand.drop_duplicates()))
user_input_brand=input("Enter the  brand = ")
model=df2.loc[df2['Brand']==user_input_brand,'Model'].copy(deep=True)
print("List of Models of  ",user_input_brand," Brand are ",list(model.drop_duplicates()))
user_input_model=input("Enter the  model = ")
memory=df2.loc[(df2['Model']==user_input_model)&(df2['Brand']==user_input_brand),'Memory']
print("List of Memory ",list(memory.drop_duplicates()))
user_input_memory=input("Enter the memory = ")
storage=df2.loc[(df2['Model']==user_input_model)&(df2['Brand']==user_input_brand)&(df2['Memory']==user_input_memory),'Storage']
print("List of Storages :",list(storage.drop_duplicates()))
user_input_storage=input("Ener the Storage = ")
user_rating=float(input("Enter the Rating "))

if((user_input_brand in list(brand.drop_duplicates())) & (user_input_model in list(model.drop_duplicates())) & (user_input_memory in list(memory.drop_duplicates())) & (user_input_storage in list(storage.drop_duplicates()))):
  error=1
else:
   error=0

print(error)



if error==1:
  user_brand_encoded = label_encoders['Brand'].transform([user_input_brand])[0]
  user_model_encoded = label_encoders['Model'].transform([user_input_model])[0]
  user_memory_encoded = label_encoders['Memory'].transform([user_input_memory])[0]
  user_storage_encoded = label_encoders['Storage'].transform([user_input_storage])[0]
  ##user_color_encoded = label_encoders['Color'].transform([user_input_color])[0]
else:
  print("error in inputs")

print(user_storage_encoded)

#Original price
if error==1:
  slr_or=DecisionTreeRegressor()
  a1=df2[['Brand_encoded','Model_encoded','Memory_encoded','Storage_encoded']];
  b1=df2['Original Price'];
  a1_train,a1_test,b1_train,b1_test=train_test_split(a1,b1,test_size=0.2,random_state=2)
  slr_or.fit(a1_train,b1_train);
  b_predi_org=slr_or.predict(a1_test)
  print(r2_score(b1_test,b_predi_org))
  original_predict=slr_or.predict([[user_brand_encoded,user_model_encoded,user_memory_encoded,user_storage_encoded]])
  print(original_predict)

## RATING
if error==1:
  slr_rat=RandomForestRegressor()
  a=df2[['Brand_encoded','Model_encoded','Memory_encoded','Storage_encoded','Original Price']];
  b=df2['Rating'];
  a_train,a_test,b_train,b_test=train_test_split(a,b,test_size=0.3,random_state=2)
  slr_rat.fit(a_train,b_train);
  b_predi_rat=slr_rat.predict(a_test)
  print(r2_score(b_test,b_predi_rat))
  origina= list(df2.loc[(df2['Brand_encoded'] == user_brand_encoded)&(df2['Model_encoded']==user_model_encoded)&(df2['Memory_encoded']==user_memory_encoded)|(df2['Storage_encoded']==user_storage_encoded),'Original Price'])
  origina=mean(origina)
  use_rating=slr_rat.predict([[user_brand_encoded,user_model_encoded,user_memory_encoded,user_storage_encoded,original_predict[0]]])
  print(use_rating)

if error==1:
  rf=RandomForestRegressor()
  rf.fit(x_train,y_train);
  ##df4=df2.drop_duplicates(subset=[''])
  ##df2.drop_duplicates(subset=['Brand','Model','Memory','Storage'],inplace=True)
  original= list(df2.loc[(df2['Brand_encoded'] == user_brand_encoded)&(df2['Model_encoded']==user_model_encoded)&(df2['Memory_encoded']==user_memory_encoded)|(df2['Storage_encoded']==user_storage_encoded),'Original Price'])
  ##print(original)
  rating=list(df2.loc[(df2['Brand_encoded']==user_brand_encoded)&(df2['Model_encoded']==user_model_encoded)|(df2['Memory_encoded']==user_memory_encoded),'Rating'])
  original=mean(original)
  ##print(original)
  ##print("Original Price :",original[0],"\n","Rating :",rating[0])
  ##print(user_brand_encoded," ",user_model_encoded," ",user_color_encoded," ",user_memory_encoded," ",user_storage_encoded," ",rating," ",original)
  print("Original Price :",original_predict,"Rating :",user_rating)
  s_p=rf.predict([[user_brand_encoded,user_model_encoded,user_memory_encoded,user_storage_encoded,user_rating,original_predict[0]]])
  print("Selling Price is ",s_p)
  print("Discount (%):",((original_predict[0]-s_p)/original_predict[0])*100)
  print("Rating by prediction")
  print("Original Price :",original_predict,"Rating :",use_rating)
  s_p_rat=rf.predict([[user_brand_encoded,user_model_encoded,user_memory_encoded,user_storage_encoded,use_rating[0],original_predict[0]]])
  ##s_p=slr.predict(["OPPO","A53","Blue","4 GB","64 GB",rating,original])
  print("Selling Price is ",s_p_rat)
  print("Discount (%):",((original_predict[0]-s_p_rat)/original_predict[0])*100)

import matplotlib.pyplot as plt
import seaborn as sns
plt.scatter(x.iloc[:,4],y)
plt.xlabel('Rating')
plt.ylabel('Selling Price')
plt.show()



"""###2.Random Forest Regressor"""

from sklearn.ensemble import RandomForestRegressor
if error==1:
  model=RandomForestRegressor()
  model.fit(x_train,y_train)
  rand_pred=model.predict(x_test)
  r2=r2_score(y_test,rand_pred);
  root_mean_square=np.sqrt(mean_squared_error(y_test,y_predi))
  mean_absolute=mean_absolute_error(y_test,y_predi)
  print("Random Forest Regression Algorithm")
  print("r2 score : ",r2)
  print("Root Mean Squared Error :",root_mean_square)
  print("Mean Absolute Error :",mean_absolute)
  ##sp_rf=model.predict([[user_brand_encoded,user_model_encoded,user_memory_encoded,user_storage_encoded,rating[0],original]])
  sp_rf=model.predict([[user_brand_encoded,user_model_encoded,user_memory_encoded,user_storage_encoded,user_rating,original_predict[0]]])
  #sp_rf=model.predict([[11,125,19,3,4.3,17990]])
  print("Selling Price =",sp_rf)

"""### 3.Decision Tree Regressor"""

# prompt: Decision Tree Regressor

from sklearn.tree import DecisionTreeRegressor
if error==1:
  model1 = DecisionTreeRegressor()
  model1.fit(x_train,y_train)
  y_pred1=model1.predict(x_test)
  #print(r2_score(y_test,y_pred1))
  root_mean_square=np.sqrt(mean_squared_error(y_test,y_predi))
  mean_absolute=mean_absolute_error(y_test,y_predi)
  print("Decision Tree Regression Algorithm")
  print("r2 score : ",r2)
  print("Root Mean Squared Error :",root_mean_square)
  print("Mean Absolute Error :",mean_absolute)
  #sp_dt=model1.predict([[11,125,19,3,4.3,17990]])
  ##sp_dt=model1.predict([[user_brand_encoded,user_model_encoded,user_memory_encoded,user_storage_encoded,rating[0],original]])
  sp_dt=model1.predict([[user_brand_encoded,user_model_encoded,user_memory_encoded,user_storage_encoded,user_rating,original_predict[0]]])
  print("Selling Price =",sp_dt)