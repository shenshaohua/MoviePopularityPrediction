import json
import omdb
import csv
import pandas as pd
import numpy as np
from numpy import genfromtxt
from sklearn import preprocessing
from sklearn import metrics
import matplotlib.pyplot as plt
# file = open("moviedata.txt","r")
# line = file.readline()
# line = line[1:len(line) - 2]
# rated = {}
# while line:
#     attrs = line.split(", ")
#     for attr in attrs:
#         content = attr.split(": ")
#         if len(content) >= 2: 
#             key = attr.split(": ")[0].strip('"')
#             value = attr.split(": ")[1].strip('"')
#             if key == "imdb_rating":
#                 rating = float(value)
#                 break
#     for attr in attrs:
#         content = attr.split(": ")
#         if len(content) >= 2: 
#             key = attr.split(": ")[0].strip('"')
#             value = attr.split(": ")[1].strip('"')
#             if key == "rated" and value != "N/A" :
#                 if value not in rated.keys():
#                     rated[value] = [rating, 1]
#                 else:
#                     rated[value] = [(rated[value][0]*rated[value][1]+rating)/(rated[value][1]+1),rated[value][1]+1]
#     line = file.readline()
# print(rated)
# file.close()
# file = open("moviedata.txt","r")
# line = file.readline()
# line = line[1:len(line) - 2]
# keys = []
# while line:
#     attrs = line.split(", ")
#     for attr in attrs:
#         content = attr.split(": ")
#         if len(content) >= 2: 
#             key = attr.split(": ")[0].strip('"')
#             value = attr.split(": ")[1].strip('"')
#             if key == "rated" and value not in keys:
#                 keys.append(value)
#     line = file.readline()
# print(keys)
# file.close()
D = {}
genre_set = set()
director_set = set()
writer_set = set()
actors_set = set()

f = open("moviedata.txt", "r")
for x in f:
    d = json.loads(x) 
    d.pop('plot', None)
    d.pop('poster', None)
    d.pop('language', None)
    d.pop('country', None)

    rating_lst = d["ratings"]
    rating_dict = {rating_lst[i]["source"] : rating_lst[i]["value"] for i in range(len(rating_lst))}
    d["ratings"] = rating_dict

    ##convert string of items into list
    genre_lst = d["genre"].split(', ')
    genre_set |= set(genre_lst)
    d["genre"] = genre_lst

    dire_lst = d["director"].split(', ')
    director_set |= set(dire_lst)
    d["director"] = dire_lst

    writer_lst = d["writer"].split(', ')
    writer_set |= set(writer_lst)
    d["writer"] = writer_lst

    actors_lst = d["actors"].split(', ')
    actors_set |= set(actors_lst)
    d["actors"] = actors_lst

    D[d["imdb_id"]] = d
f.close()
genre_rating = {}
rated_rating = {}
runtime_rating = {'0-60':[0,0],'60-90':[0,0],'90-120':[0,0],'>120':[0,0]}
director_rating = {}
actor_rating = {}
# count = 0
# for key in D.keys():
#     if len(D[key]['director']) > 1:
#         count +=1
# print(count)
for key in D.keys():
    rated = D[key]['rated']
    runtime = D[key]['runtime']
    if runtime != 'N/A':
        runtime = int(runtime.split()[0])
    genres = D[key]['genre']
    directors = D[key]['director']
    actors = D[key]['actors']
    if len(actors) == 1:
        actors = actors[0:1]
    elif len(actors) >= 2:
        actors = actors[:2]
    rating = float(D[key]['imdb_rating'])
    """
    rated vs rating
    """
    if  rated not in rated_rating.keys():
        rated_rating[rated] = [rating, 1]
    else:
        rated_rating[rated] = [round((rated_rating[rated][0]*rated_rating[rated][1]+rating)/(rated_rating[rated][1]+1) ,1),rated_rating[rated][1]+1]
    """
    director vs rating
    """
    for director in directors:
        if director != 'N/A':
            if  director not in director_rating.keys():
                director_rating[director] = [rating, 1]
            else:
                director_rating[director] = [round((director_rating[director][0]*director_rating[director][1]+rating)/(director_rating[director][1]+1) ,1),director_rating[director][1]+1]
    """
    genre vs rating
    """
    for genre in genres:
        if genre != 'N/A':
            if  genre not in genre_rating.keys():
                genre_rating[genre] = [rating, 1]
            else:
                genre_rating[genre] = [round((genre_rating[genre][0]*genre_rating[genre][1]+rating)/(genre_rating[genre][1]+1) ,1),genre_rating[genre][1]+1]
    """
    actors vs rating
    """
    for actor in actors:
        if actor != 'N/A':
            if  actor not in actor_rating.keys():
                actor_rating[actor] = [rating, 1]
            else:
                actor_rating[actor] = [round((actor_rating[actor][0]*actor_rating[actor][1]+rating)/(actor_rating[actor][1]+1) ,1),actor_rating[actor][1]+1]
    """
    runtime vs rating
    """
    if runtime == 'N/A':
        runtime_rating = runtime_rating
    elif  runtime >= 0 and runtime <= 60:
        runtime_rating['0-60'] = [round((runtime_rating['0-60'][0]*runtime_rating['0-60'][1]+rating)/(runtime_rating['0-60'][1]+1) ,1),runtime_rating['0-60'][1]+1]
    elif runtime > 60 and runtime <= 90:
        runtime_rating['60-90'] = [round((runtime_rating['60-90'][0]*runtime_rating['60-90'][1]+rating)/(runtime_rating['60-90'][1]+1) ,1),runtime_rating['60-90'][1]+1]
    elif runtime > 90 and runtime <= 120:
        runtime_rating['90-120'] = [round((runtime_rating['90-120'][0]*runtime_rating['90-120'][1]+rating)/(runtime_rating['90-120'][1]+1) ,1),runtime_rating['90-120'][1]+1]
    elif runtime > 120:
        runtime_rating['>120'] = [round((runtime_rating['>120'][0]*runtime_rating['>120'][1]+rating)/(runtime_rating['>120'][1]+1) ,1),runtime_rating['>120'][1]+1]
"""
codes for filtering director or actor with too few movies
"""
A = dict(D)
for key in A.keys():
    A[key]['director'] = D[key]['director'][0]
    A[key]['actors'] = D[key]['actors'][0]
    A[key]['genre'] = D[key]['genre'][0]
    A[key] = [A[key]['director'], A[key]['actors'],A[key]['genre'],A[key]['rated'],A[key]['runtime']]
data = list(A.values())
data = np.array(data)
ratings = []
for key in D.keys():
  rating = float(D[key]['imdb_rating'])
  ratings.append(rating)
ratings = np.array(ratings)
ratings = ratings/ratings.max()
le = preprocessing.LabelEncoder()
entry0 = np.unique(data[:,0])
entry1 = np.unique(data[:,1])
entry2 = np.unique(data[:,2])
entry3 = np.unique(data[:,3])
entry4 = np.unique(data[:,4])
le.fit(entry0)
data[:,0]=le.transform(data[:,0])
le.fit(entry1)
data[:,1]=le.transform(data[:,1])
le.fit(entry2)
data[:,2]=le.transform(data[:,2])
le.fit(entry3)
data[:,3]=le.transform(data[:,3])
le.fit(entry4)
data[:,4]=le.transform(data[:,4])
data = data.astype('float64')
data = data/data.max(axis = 0)
print(data)
from sklearn.model_selection import train_test_split
X = data
y = ratings
X_train, X_test, y_train, y_test = train_test_split(X, y)

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

# Fit only to the training data
scaler.fit(X_train)

StandardScaler(copy=True, with_mean=True, with_std=True)

# Now apply the transformations to the data:
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

from sklearn.neural_network import MLPRegressor
mlp = MLPRegressor(hidden_layer_sizes=(13,13,13),max_iter=500)
y_train = y_train.astype('float64')
mlp.fit(X_train,y_train)
MLPRegressor(activation='relu', alpha=0.0001, batch_size='auto',
            epsilon=1e-8, learning_rate_init=0.0001)
y_pred = mlp.predict(X_test)

print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

print('R2 score:', mlp.score(X_test, y_test))
plt.scatter(y_test, y_pred, color='black')
x=np.linspace(-0.1,1,1000)
plt.plot(x, x, color='red')
plt.xlabel("Actual Rating")
plt.ylabel("Predicted Rating")
plt.show()