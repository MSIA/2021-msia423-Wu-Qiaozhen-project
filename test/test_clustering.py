import pytest
import pandas as pd
import numpy as np
from src.clustering import *

df_in_values =[[ 0.2747406 ,  0.54596633,  1.64652881,  0.77970168, -1.27979342,
                 -0.56096905, -0.05022138, -0.32474622, -0.64663628,  0.52078926,
                 0.99677181],
               [-0.94234649,  0.9172987 , -1.13888337,  1.06431895,  0.78137611,
                1.41182299, -0.75713602, -0.32470328, -0.80024225,  1.1813218 ,
                2.46081597],
               [ 0.43048161,  0.50618072, -1.41742458,  0.72200318,  0.78137611,
                 -0.62436691,  1.27905044, -0.32474622, -0.68668537,  0.28667645,
                 -0.94815947],
               [-1.33458309,  0.20999894, -0.30325971,  0.8279273 , -1.27979342,
                -0.50204634,  0.91717321, -0.32474622, -0.36730661, -0.75010881,
                -0.80233917],
               [ 0.24013149, -0.13480969,  0.53236394,  1.06302719,  0.78137611,
                 -0.29395221, -0.50525513, -0.32474622, -0.71456764,  0.37446875,
                 -0.62992074],
               [ 0.63236809,  0.93056057,  0.53236394,  1.10457872, -1.27979342,
                 -0.61840005,  0.30448997, -0.32470131, -0.57008677, -0.01014513,
                 -0.73787783],
               [ 0.47662709, -0.21438092, -0.30325971,  0.43846238, -1.27979342,
                 -0.62884205,  0.11459399, -0.32470894, -0.58022578,  0.33684348,
                 -0.91060917],
               [-0.67124178,  0.81562436,  1.64652881,  0.6361013 , -1.27979342,
                -0.06497408, -0.8769138 , -0.32474622,  0.52999559, -0.86298462,
                -0.95706028],
               [ 0.04401319,  0.58575194, -0.30325971,  0.34933111,  0.78137611,
                 -0.46027834, -0.90918895, -0.32467297, -0.58529529, -0.88388755,
                 -0.18216828],
               [ 0.89193643,  0.85540997, -1.13888337,  1.02384387,  0.78137611,
                 0.61375589, -0.90414417, -0.29771407, -0.68769927, -0.1648268 ,
                 -0.04399711]]

df_in_index = [1,2,3,4,5,6,7,8,9,10]

df_in_columns = ['danceability','energy','key','loudness','mode','speechiness','acousticness','instrumentalness',
                 'liveness','valence','tempo']

df_in = pd.DataFrame(df_in_values, index=df_in_index, columns=df_in_columns)

songs_list= ["artist","release_date","track_name","danceability",
             "energy","key","loudness","mode","speechiness","acousticness",
             "instrumentalness","liveness","valence","tempo","type"]

selected_columns = [ "danceability","energy","key","loudness","mode","speechiness",
                     "acousticness","instrumentalness","liveness","valence","tempo" ]

def test_quick_result():
    labels_new, df_summary_new = quick_result(df_in, 8, 36)
    grand_mean = df_in.mean(axis=0).values
    mod = KMeans(n_clusters=8, random_state=36).fit(df_in)
    df_summary, _ = summary_kmeans(df_in, mod, grand_mean)
    for i in range(0,10):
        assert mod.labels_[i] == labels_new[i]
    pd.testing.assert_frame_equal(df_summary_new, df_summary)

def test_quick_result_non_df():
    df_in = 'I am not a dataframe'

    with pytest.raises(AttributeError):
        quick_result(df_in, 8, 36)