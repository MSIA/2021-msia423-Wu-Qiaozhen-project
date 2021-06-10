import pytest
import pandas as pd
import numpy as np
from src.get_para import *

df_in_values =[[0.649, 0.767, 11.0, -3.838, 0.0, 0.0455, 0.24, 0.0, 0.0929, 0.608,
                149.918, 1, '6kKC35sKUh2FUx4M0qAL44',
                'spotify:track:6kKC35sKUh2FUx4M0qAL44',
                'https://api.spotify.com/v1/tracks/6kKC35sKUh2FUx4M0qAL44',
                'https://api.spotify.com/v1/audio-analysis/6kKC35sKUh2FUx4M0qAL44',
                227173.0, 4.0, 'Candy', 'Delight - The 2nd Mini Album',
                'Delight - The 2nd Mini Album', '2020-05-25',
                '75sPv82oaDKYjtuuS4l3Vc', 'BAEKHYUN_k'],
               [0.6759999999999999, 0.758, 0.0, -4.106, 1.0, 0.037000000000000005,
                0.611, 0.0, 0.085, 0.552, 93.979, 1, '6wwmbBoBaFxptJwuvF2QdM',
                'spotify:track:6wwmbBoBaFxptJwuvF2QdM',
                'https://api.spotify.com/v1/tracks/6wwmbBoBaFxptJwuvF2QdM',
                'https://api.spotify.com/v1/audio-analysis/6wwmbBoBaFxptJwuvF2QdM',
                206693.0, 4.0, 'Bungee', 'Delight - The 2nd Mini Album',
                'Delight - The 2nd Mini Album', '2020-05-25',
                '75sPv82oaDKYjtuuS4l3Vc', 'BAEKHYUN_k'],
               [0.43799999999999994, 0.851, 1.0, -2.516, 1.0, 0.31, 0.0427,
                9.85e-06, 0.0626, 0.7659999999999999, 192.02599999999998, 1,
                '4Jxc98fY5SQ6zyGg8Dnybw', 'spotify:track:4Jxc98fY5SQ6zyGg8Dnybw',
                'https://api.spotify.com/v1/tracks/4Jxc98fY5SQ6zyGg8Dnybw',
                'https://api.spotify.com/v1/audio-analysis/4Jxc98fY5SQ6zyGg8Dnybw',
                174507.0, 4.0, 'R U Ridin’?', 'Delight - The 2nd Mini Album',
                'Delight - The 2nd Mini Album', '2020-05-25',
                '75sPv82oaDKYjtuuS4l3Vc', 'BAEKHYUN_k'],
               [0.37, 0.691, 4.0, -3.614, 0.0, 0.0534, 0.51, 0.0,
                0.14800000000000002, 0.304, 98.17299999999999, 1,
                '7tIFeLQFS7A6DLcZ12Mv3U', 'spotify:track:7tIFeLQFS7A6DLcZ12Mv3U',
                'https://api.spotify.com/v1/tracks/7tIFeLQFS7A6DLcZ12Mv3U',
                'https://api.spotify.com/v1/audio-analysis/7tIFeLQFS7A6DLcZ12Mv3U',
                199187.0, 4.0, 'Underwater', 'Delight - The 2nd Mini Album',
                'Delight - The 2nd Mini Album', '2020-05-25',
                '75sPv82oaDKYjtuuS4l3Vc', 'BAEKHYUN_k'],
               [0.643, 0.613, 7.0, -2.522, 1.0, 0.0813, 0.113, 0.0, 0.0795, 0.573,
                103.132, 1, '1JTUPJr0rSf93hNlRR6S0g',
                'spotify:track:1JTUPJr0rSf93hNlRR6S0g',
                'https://api.spotify.com/v1/tracks/1JTUPJr0rSf93hNlRR6S0g',
                'https://api.spotify.com/v1/audio-analysis/1JTUPJr0rSf93hNlRR6S0g',
                208267.0, 4.0, 'Poppin’', 'Delight - The 2nd Mini Album',
                'Delight - The 2nd Mini Album', '2020-05-25',
                '75sPv82oaDKYjtuuS4l3Vc', 'BAEKHYUN_k'],
               [0.711, 0.8540000000000001, 7.0, -2.329, 0.0, 0.0378,
                0.33899999999999997, 1.0300000000000001e-05, 0.10800000000000001,
                0.48100000000000004, 100.027, 1, '4pulHxja8nTUiojRtfwgTv',
                'spotify:track:4pulHxja8nTUiojRtfwgTv',
                'https://api.spotify.com/v1/tracks/4pulHxja8nTUiojRtfwgTv',
                'https://api.spotify.com/v1/audio-analysis/4pulHxja8nTUiojRtfwgTv',
                204253.0, 4.0, 'Ghost', 'Delight - The 2nd Mini Album',
                'Delight - The 2nd Mini Album', '2020-05-25',
                '75sPv82oaDKYjtuuS4l3Vc', 'BAEKHYUN_k'],
               [0.684, 0.595, 4.0, -5.422999999999999, 0.0, 0.0364,
                0.28600000000000003, 8.55e-06, 0.106, 0.564, 95.059, 1,
                '4dYODiAYvJHWQJtNganYCY', 'spotify:track:4dYODiAYvJHWQJtNganYCY',
                'https://api.spotify.com/v1/tracks/4dYODiAYvJHWQJtNganYCY',
                'https://api.spotify.com/v1/audio-analysis/4dYODiAYvJHWQJtNganYCY',
                205293.0, 4.0, 'Love Again', 'Delight - The 2nd Mini Album',
                'Delight - The 2nd Mini Album', '2020-05-25',
                '75sPv82oaDKYjtuuS4l3Vc', 'BAEKHYUN_k'],
               [0.485, 0.828, 11.0, -4.505, 0.0, 0.11199999999999999, 0.00927, 0.0,
                0.325, 0.27699999999999997, 93.723, 1, '41sIKltzKnhFsDXWTKjO3R',
                'spotify:track:41sIKltzKnhFsDXWTKjO3R',
                'https://api.spotify.com/v1/tracks/41sIKltzKnhFsDXWTKjO3R',
                'https://api.spotify.com/v1/audio-analysis/41sIKltzKnhFsDXWTKjO3R',
                358271.0, 4.0, 'So Far Away', 'Agust D', 'Agust D', '2016-08-16',
                '6GbiSEYL78RDLpxoxkWavo', 'augustd_k'],
               [0.609, 0.7759999999999999, 4.0, -5.837000000000001, 1.0,
                0.059000000000000004, 0.000262, 1.6800000000000002e-05, 0.105,
                0.272, 116.01, 1, '4rEP3s8gClYCL1rKUKX4M0',
                'spotify:track:4rEP3s8gClYCL1rKUKX4M0',
                'https://api.spotify.com/v1/tracks/4rEP3s8gClYCL1rKUKX4M0',
                'https://api.spotify.com/v1/audio-analysis/4rEP3s8gClYCL1rKUKX4M0',
                207874.0, 4.0, 'Tony Montana', 'Agust D', 'Agust D', '2016-08-16',
                '6GbiSEYL78RDLpxoxkWavo', 'augustd_k'],
               [0.7559999999999999, 0.8370000000000001, 1.0, -2.7039999999999997,
                1.0, 0.203, 0.0016699999999999998, 0.0062, 0.0848, 0.444, 119.984,
                1, '6lRWD0dOKIrFrmb9tmd62M',
                'spotify:track:6lRWD0dOKIrFrmb9tmd62M',
                'https://api.spotify.com/v1/tracks/6lRWD0dOKIrFrmb9tmd62M',
                'https://api.spotify.com/v1/audio-analysis/6lRWD0dOKIrFrmb9tmd62M',
                245757.0, 4.0, 'The Last', 'Agust D', 'Agust D', '2016-08-16',
                '6GbiSEYL78RDLpxoxkWavo', 'augustd_k']]

df_in_index = [1,2,3,4,5,6,7,8,9,10]

df_in_columns = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
                 'type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms',
                 'time_signature', 'track_name', 'album_name', 'short_album_name',
                 'release_date', 'album_id', 'artist']

df_in = pd.DataFrame(df_in_values, index=df_in_index, columns=df_in_columns)

songs_list= ["artist","release_date","track_name","danceability",
              "energy","key","loudness","mode","speechiness","acousticness",
              "instrumentalness","liveness","valence","tempo","type"]

selected_columns = [ "danceability","energy","key","loudness","mode","speechiness",
                     "acousticness","instrumentalness","liveness","valence","tempo" ]

def test_subset():
    test_new = subset(df_in,songs_list)
    test = df_in[songs_list]
    pd.testing.assert_frame_equal(test_new, test)

def test_subset_non_df():
    df_in = 'I am not a dataframe'

    with pytest.raises(TypeError):
        subset(df_in,songs_list)

def test_scale():
    test_new = scale(df_in, selected_columns)

    df = df_in.filter(selected_columns)
    scaler = StandardScaler()
    array_scaled = scaler.fit_transform(df)
    df_scaled = pd.DataFrame(array_scaled)
    df_scaled.columns = list(df.columns)
    pd.testing.assert_frame_equal(test_new, df_scaled)

def test_scale_non_df():
    df_in = 'I am not a dataframe'

    with pytest.raises( AttributeError):
        scale(df_in,selected_columns)

def test_get_a_mod_list_and_dict():
    cluster_range = [7,8,9,10]
    list_new = get_a_mod_list_and_dict(df_in[selected_columns], cluster_range, seed=36)

    mod_dict = {}
    for k in cluster_range:
        mod = KMeans(n_clusters=k, random_state=36).fit(df_in[selected_columns])
        mod_dict[str(k)] = mod
    mod_list = list(mod_dict.values())
    assert np.allclose(list_new[0].labels_, mod_list[0].labels_)
    assert list_new[1].inertia_ ==  mod_list[1].inertia_

def test_get_a_mod_list_and_dict_non_df():
    df_in = 'I am not a dataframe'
    cluster_range = [7,8,9,10]

    with pytest.raises(TypeError):
        get_a_mod_list_and_dict(df_in[selected_columns], cluster_range, seed=36)

