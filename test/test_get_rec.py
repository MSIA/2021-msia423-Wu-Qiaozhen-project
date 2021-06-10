import pytest
import pandas as pd
import numpy as np
from src.get_rec import *

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
                0.14800000000000002, 0.304, 98.17299999999999, 0,
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
                0.48100000000000004, 100.027, 0, '4pulHxja8nTUiojRtfwgTv',
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
                0, '6lRWD0dOKIrFrmb9tmd62M',
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

mod_labels = [1,2,3,3,2,1,3,2,2,1]

e_song_z_values = [[0.04584651292936117, 1.2567010459485368, 1.1142882827393972,
                    1.0464087425756563, 0.743830305511655, -0.6023550793026846,
                    -0.8665648206826251, -0.4214982675467285, -0.551414557217183,
                    -0.6653280026739604, 0.32403745549715796, 'Better Left Unsaid',
                    '2013-01-01', 'arianagrande', 6],
                   [0.7118659156525323, 1.1007680940693179, -1.133494017583932,
                    1.1138659942893971, 0.743830305511655, -0.6036995311004106,
                    -0.9466348980683601, -0.4220089979143289, 1.1858375720737475,
                    0.2579049091565112, -0.627674355288964, 'Baby I', '2013-01-01',
                    'arianagrande', 1],
                   [0.5440900355772301, 0.23855059544304966, 0.833315495198981,
                    0.8065386916288549, -1.344392655946083, -0.5472325555959223,
                    -0.27905474669593533, -0.4220089979143289, 1.1441435209707653,
                    -0.010384996845506205, 0.1546978263279482, 'Honeymoon Avenue',
                    '2013-01-01', 'arianagrande', 5],
                   [0.1831176875364271, 1.2750460991107984, 0.5523427076585649,
                    1.216639101312096, 0.743830305511655, -0.11700798032363,
                    -0.5789056537783176, -0.4220089979143289, -0.6806661156364283,
                    0.43150426009899323, 1.2103704483629576, 'Right There',
                    '2013-01-01', 'arianagrande', 4],
                   [-0.24903230659692804, -0.16045431083612763, 0.5523427076585649,
                    1.025774759698512, 0.743830305511655, -0.6386552778412844,
                    0.3535977165987614, -0.4220089979143289, -0.2873522335649617,
                    -0.5430193690553937, -1.6437121303042246, 'Tattooed Heart',
                    '2013-01-01', 'arianagrande', 2],
                   [0.41190297854820307, 1.164975780137232, 0.833315495198981,
                    0.9372867177446053, 0.743830305511655, -0.5149657124505004,
                    -0.4965290309534873, -0.4220089979143289, -0.8481372209000742,
                    1.4178642086358215, -0.7279671601298541, 'Popular Song',
                    '2013-01-01', 'arianagrande', 6],
                   [0.7779594441670455, 1.1374582003938405, -1.133494017583932,
                    0.9944269780197738, -1.344392655946083, -0.270947711163247,
                    -0.46028331691056196, -0.4220089979143289, 4.4657695921750244,
                    1.0469928679859744, -0.014947470041928023, 'Piano', '2013-01-01',
                    'arianagrande', 7],
                   [0.19837004027054553, 1.2154246763334495, -1.133494017583932,
                    1.082121405247637, -1.344392655946083, -0.5391658448095668,
                    -0.6283316274732158, -0.4220089979143289, 0.6438149077349775,
                    -0.010384996845506205, -0.8991068294807666, "Lovin' It",
                    '2013-01-01', 'arianagrande', 5],
                   [-1.3268652331412967, -1.0501893892057876, -0.8525212300435159,
                    0.35794796773247933, 0.743830305511655, -0.5479047814947852,
                    1.7210496554909442, -0.4220089979143289, -0.5722615827686743,
                    -0.4641105731724476, -1.3289428396623795, 'Almost Is Never Enough',
                    '2013-01-01', 'arianagrande', 2],
                   [0.910146501196072, 1.3117362054353205, 0.2713699201181487,
                    1.0839070383812357, 0.743830305511655, -0.42623189380058996,
                    -0.8174683534790261, -0.4220089979143289, -1.0302012440497637,
                    1.6466997166963664, -0.5244607305305946, 'You’ll Never Know',
                    '2013-01-01', 'arianagrande', 6]]

e_song_z_index = [1,2,3,4,7,1,5,0,4,6]

e_song_z_columns = ['danceability','energy','key','loudness','mode','speechiness','acousticness','instrumentalness','liveness',
                    'valence','tempo','track_name','release_date','artist','class']

e_songs_z = pd.DataFrame(e_song_z_values, index=e_song_z_index, columns=e_song_z_columns)

k_song_z_values = [[0.19135012084500205, 0.022009209234688236, 1.6075273978078195,
                    0.476848851165664, -1.1986501683016801, -0.6575529125993184,
                    0.2329223542068015, -0.1428703141568809, -0.7318281216965948,
                    0.3851924176122856, 0.9935349066962128, 'Candy', '2020-05-25',
                    'BAEKHYUN_k', 5],
                   [-1.408762193546728, 0.4963483102479106, -1.1466545915593835,
                    1.0454468567730324, 0.834271772069127, 1.7283817071053804,
                    -0.6423040354496744, -0.14275798598673767, -0.8562179413360066,
                    1.1354714443254617, 2.510111241648271, 'R U Ridin’?', '2020-05-25',
                    'BAEKHYUN_k', 4],
                   [0.3961038293216682, -0.028812837302442797, -1.422072790496104,
                    0.3615808742346696, 0.834271772069127, -0.734227560113458,
                    1.8786851041437125, -0.1428703141568809, -0.764259790843504,
                    0.11927073725824869, -1.0211835221268903, 'Bungee', '2020-05-25',
                    'BAEKHYUN_k', 1],
                   [-1.924438200080555, -0.4071547393010849, -0.3203999947492227,
                    0.5731922348691819, -1.1986501683016801, -0.5862905931450003,
                    1.4306472665598096, -0.1428703141568809, -0.5056274925833409,
                    -1.058382418595345, -0.87013096325948, 'Underwater', '2020-05-25',
                    'BAEKHYUN_k', 5],
                   [0.14584929673907607, -0.8476124759562199, 0.5058546020609382,
                    1.042866230423831, 0.834271772069127, -0.33461733836329494,
                    -0.3304519564185023, -0.1428703141568809, -0.7868388010090739,
                    0.21899136739101221, -0.6915258990192575, 'Poppin’', '2020-05-25',
                    'BAEKHYUN_k', 6],
                   [0.6615253032729033, 0.5132889924269549, 0.5058546020609382,
                    1.1258763779898082, -1.1986501683016801, -0.7270111227003625,
                    0.6720881554029043, -0.14275285424292403, -0.6698384756056668,
                    -0.2178799646191914, -0.803356656120667, 'Ghost', '2020-05-25',
                    'BAEKHYUN_k', 5],
                   [0.4567715947962371, -0.9492565690304821, -0.3203999947492227,
                    -0.20486660941503057, -1.1986501683016801, -0.7396398881732796,
                    0.4369791911262031, -0.14277281102442155, -0.6780490247567832,
                    0.17625395447697048, -0.982285867482922, 'Love Again',
                    '2020-05-25', 'BAEKHYUN_k', 5],
                   [-1.0523390713836411, 0.3664697468752424, 1.6075273978078195,
                    0.18996922201277858, -1.1986501683016801, -0.05768655263575529,
                    -0.7906001236717524, -0.1428703141568809, 0.2210061072904506,
                    -1.1865946573374702, -1.0304037069313867, 'So Far Away',
                    '2016-08-16', 'augustd_k', 5],
                   [-0.11198870652783793, 0.07283125577181865, -0.3203999947492227,
                    -0.38292982750992566, 0.834271772069127, -0.5357755312533319,
                    -0.8305597755624038, -0.14267872905450463, -0.6821542993323413,
                    -1.2103376645119375, -0.22770738373682634, 'Tony Montana',
                    '2016-08-16', 'augustd_k', 1],
                   [1.0027814840673475, 0.41729179341237405, -1.1466545915593835,
                    0.9645872311647229, 0.834271772069127, 0.7631832031038578,
                    -0.8243138619453926, -0.07216628827993474, -0.7650808457586158,
                    -0.39357821771025187, -0.08457842118577984, 'The Last',
                    '2016-08-16', 'augustd_k', 1]]

k_song_z_index = [1,2,3,4,5,6,7,1,0,3]

k_song_z_columns = ['danceability','energy','key','loudness','mode','speechiness','acousticness','instrumentalness','liveness',
                    'valence','tempo','track_name','release_date','artist','class']

k_songs_z = pd.DataFrame(k_song_z_values, index=k_song_z_index, columns=k_song_z_columns)

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

    with pytest.raises(AttributeError):
        scale(df_in,selected_columns)

def test_get_cluster_df():
    k_songs_z_new, e_songs_z_new  = get_cluster_df(df_in, mod_labels, selected_columns)
    songs_df = df_in.dropna()
    songs_df["class"] = mod_labels
    e_songs = songs_df[songs_df["type"] == 0]
    k_songs = songs_df[songs_df["type"] == 1]

    print(e_songs)

    e_songs_z = scale(e_songs[selected_columns], selected_columns)
    k_songs_z = scale(k_songs[selected_columns], selected_columns)

    e_songs_z["track_name"] = e_songs["track_name"].tolist()
    e_songs_z["release_date"] = e_songs["release_date"].tolist()
    e_songs_z["artist"] = e_songs["artist"].tolist()
    e_songs_z["class"] = e_songs["class"].tolist()

    k_songs_z["track_name"] = k_songs["track_name"].tolist()
    k_songs_z["release_date"] = k_songs["release_date"].tolist()
    k_songs_z["artist"] = k_songs["artist"].tolist()
    k_songs_z["class"] = k_songs["class"].tolist()

    k_songs_z = k_songs_z.drop_duplicates()
    e_songs_z = e_songs_z.drop_duplicates()

    pd.testing.assert_frame_equal(k_songs_z, k_songs_z_new)
    pd.testing.assert_frame_equal(e_songs_z, e_songs_z_new)

def test_get_cluster_df_non_df():
    df_in = 'I am not a dataframe'

    with pytest.raises(AttributeError):
        get_cluster_df(df_in, mod_labels, selected_columns)

def test_dist():
    song1 = df_in.iloc[0]
    song2 = df_in.iloc[1]
    dist_new = dist(song1, song2)

    sqr_d = np.square(np.array(song1[selected_columns].tolist()) - np.array(song2[selected_columns].tolist()))
    distance = sqr_d.sum()
    assert dist_new == distance

def test_dist_non_df():
    song1 = 'I am not a dataframe'
    song2 = 'I am not a dataframe'

    with pytest.raises(TypeError):
        dist(song1, song2)


def test_get_closest_list_non_df():
    song1 = 'I am not a dataframe'
    song2 = 'I am not a dataframe'

    with pytest.raises(ValueError):
        get_closest_list(k_songs_z, e_songs_z)

