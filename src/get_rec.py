import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


def load_songs(df, subset_l):
    """subset songs dataframe from dataset

    Args:
        df(pd.Dataframe):obj:`pandas.DataFrame` initial dataset
        subset_l(list): list of columns that are included in the features

    Returns:
        df_sub (:obj:`pandas.DataFrame`): subseted dataframe
    """
    df_sub = df[subset_l]
    return df_sub


def load_labels(path):
    """subset songs dataframe from dataset

    Args:
        path(String): path the load the labels

    Returns:
        labels(np.array): numpy array of labels
    """
    labels = np.array(pd.read_csv(path, header=None))
    return labels


def scale(df, selected_columns):
    """scale the scores in the df

    Args:
        df(pd.Dataframe):obj:`pandas.DataFrame` initial dataset
        selected_columns(list): list of columns that are included in the features

    Returns:
        df_scaled (:obj:`pandas.DataFrame`): scaled dataframe

    """
    df = df.filter(selected_columns)
    scaler = StandardScaler()
    array_scaled = scaler.fit_transform(df)
    df_scaled = pd.DataFrame(array_scaled)
    df_scaled.columns = list(df.columns)
    return df_scaled


def get_cluster_df(df_song, mod_labels, selected_columns):
    """produce dataframe of kpop songs and English songs with class labels

    Args:
        df_song(pd.Dataframe):obj:`pandas.DataFrame` initial dataset of the songs
        mod_labels(np.array): numpy array of labels
        selected_columns(list): list of columns that are included in the features

    Returns:
        k_songs_z(pd.Dataframe):obj:`pandas.DataFrame`:dataframe of kpop songs
        e_songs_z(pd.Dataframe):obj:`pandas.DataFrame`:dataframe of English songs
    """
    songs_df = df_song.dropna()
    songs_df["class"] = mod_labels
    e_songs = songs_df[songs_df["type"] == 0]
    k_songs = songs_df[songs_df["type"] == 1]

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

    return k_songs_z, e_songs_z


def dist(song1, song2):
    selected_columns = ["danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness",
                        "instrumentalness", "liveness", "valence", "tempo"]
    sqr_d = np.square(np.array(song1[selected_columns].tolist()) - np.array(song2[selected_columns].tolist()))
    return sqr_d.sum()


def get_closest_list(k_songs_z, e_songs_z):
    """produce list of corresponding closest kpop songs to English songs

    Args:
        k_songs_z(pd.Dataframe):obj:`pandas.DataFrame`:dataframe of kpop songs
        e_songs_z(pd.Dataframe):obj:`pandas.DataFrame`:dataframe of English songs

    Returns:
        closest_list(List): list of name and artist of the closest song
    """
    cluster_0 = k_songs_z[k_songs_z["class"] == 0]
    cluster_1 = k_songs_z[k_songs_z["class"] == 1]
    cluster_2 = k_songs_z[k_songs_z["class"] == 2]
    cluster_3 = k_songs_z[k_songs_z["class"] == 3]
    cluster_4 = k_songs_z[k_songs_z["class"] == 4]
    cluster_5 = k_songs_z[k_songs_z["class"] == 5]
    cluster_6 = k_songs_z[k_songs_z["class"] == 6]
    cluster_7 = k_songs_z[k_songs_z["class"] == 7]

    closest_list = []
    for i in range(0, e_songs_z.shape[0]):
        e_song = e_songs_z.iloc[i]
        cluster_num = e_song["class"]

        if cluster_num == 0:
            cluster = cluster_0
        if cluster_num == 1:
            cluster = cluster_1
        if cluster_num == 2:
            cluster = cluster_2
        if cluster_num == 3:
            cluster = cluster_3
        if cluster_num == 4:
            cluster = cluster_4
        if cluster_num == 5:
            cluster = cluster_5
        if cluster_num == 6:
            cluster = cluster_6
        if cluster_num == 7:
            cluster = cluster_7

        dist_dict = {}
        for j in range(0, cluster.shape[0]):
            k_song = cluster.iloc[j]
            dist_dict[k_song["track_name"] + "===" + k_song["artist"]] = dist(e_song, k_song)

        mini = min(dist_dict.values())
        name = [key for key in dist_dict if dist_dict[key] == mini][0]

        closest_list.append(name)
    return closest_list


def get_final_rds(k_songs_z, e_songs_z):
    """produce list of corresponding closest kpop songs to English songs

    Args:
        k_songs_z(pd.Dataframe):obj:`pandas.DataFrame`:dataframe of kpop songs
        e_songs_z(pd.Dataframe):obj:`pandas.DataFrame`:dataframe of English songs

    Returns:
        e_k_merged(pd.Dataframe):obj:`pandas.DataFrame`: merged dataset of English songs and recommended kpop songs
    """
    closest_list = get_closest_list(k_songs_z, e_songs_z)
    song_l = []
    artist_l = []
    for item in closest_list:
        list_i = item.split("===")
        song_l.append(list_i[0])
        artist_l.append(list_i[1])

    e_songs_z["k_closest_song"] = song_l
    e_songs_z["k_closest_artist"] = artist_l

    e_k_merged = e_songs_z.merge(k_songs_z, left_on=["k_closest_song", "k_closest_artist"],
                                 right_on=["track_name", "artist"], how="inner").drop_duplicates()
    return e_k_merged


def store_rds(e_k_merged, path):
    """Store subseted scaled dataframe to local

    Args:
        e_k_merged(pd.Dataframe):obj:`pandas.DataFrame` merged dataframe
        path(String): path to store the datafarme

    Returns:
        None

    """
    rds = e_k_merged[["track_name_x", "artist_x", "track_name_y", "artist_y"]]
    rds.to_csv(path, index=False)
