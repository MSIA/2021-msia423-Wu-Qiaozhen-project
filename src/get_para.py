import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


def subset(df, songs_list):
    """subset the dataframe with songs_list

    Args:
        df(pd.Dataframe):obj:`pandas.DataFrame` initial dataset
        songs_list(list): list of columns song names that are included in the features

    Returns:
        df_subset (:obj:`pandas.DataFrame`): updated dataframe

    """
    df_subset = df[songs_list]
    return df_subset


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


def get_a_mod_list_and_dict(df, cluster_range, seed=36):
    """produce list of mods according to a range of cluster numbers

    Args:
        df(pd.Dataframe):obj:`pandas.DataFrame` initial dataset
        cluster_range(List): list of cluster numbers tested on
        seed(int): set seed for the kmeans function

    Returns:
        mod_list (list): list of mod tested

    """
    mod_dict = {}
    for k in cluster_range:
        mod = KMeans(n_clusters=k, random_state=seed).fit(df)
        mod_dict[str(k)] = mod
    mod_list = list(mod_dict.values())
    return mod_list


#used for plotting, so there's no testing for this
def summary_kmeans(df, mod):
    """produce kmeans summary and F score

    Args:
        df(pd.Dataframe):obj:`pandas.DataFrame` initial dataset
        mod(KMeans):obj: input kmeans mod

    Returns:
        df(pd.Dataframe):obj:`pandas.DataFrame` dataframe of cluster centers
        F(double): F score

    """
    grand_mean = df.mean(axis=0).values
    df_summary = pd.DataFrame(mod.cluster_centers_, columns=list(df.columns))
    df_summary['count'] = pd.Series(mod.labels_).value_counts().sort_index()  # fix typo here
    df_summary['percent'] = df_summary['count'] / df_summary['count'].sum()
    columns_ordered = ['count', 'percent'] + list(df.columns)
    df_summary = df_summary[columns_ordered]

    # calculate the F statistics
    n = sum(df_summary["count"])
    k = len(df_summary)
    SSB = 0
    for index, row in df_summary.iterrows():
        n_cur = row["count"]
        SSB += n_cur * np.sum((row[2:] - grand_mean) ** 2)
    MSB = SSB / (k - 1)
    MSE = mod.inertia_ / (n - k)
    F = MSB / MSE
    return df_summary, F


#used for plotting, so there's no testing for this
def cluster_selection_plot(df, mod_list, cluster_range):
    """produce plots for within_ss, silhuoette score and F score

    Args:
        df(pd.Dataframe):obj:`pandas.DataFrame` initial dataset
        mod_list(List): list of kmeans mod
        cluster_range(List): list of cluster numbers tested on

    Returns:
        None

    """

    F_list = [summary_kmeans(df, mod)[1] for mod in mod_list]
    within_ss = [i.inertia_ for i in mod_list]
    silhouette_list = [silhouette_score(df, i.labels_) for i in mod_list]

    fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))
    axs[0].plot(cluster_range, within_ss, color='royalblue')
    axs[1].plot(cluster_range, silhouette_list, color='green')
    axs[2].plot(cluster_range, F_list, color='red')

    for i in range(3):
        axs[i].set_xlabel('number of clusters')
    for idx, name in zip([0, 1, 2], ['within_ss', 'silhouette score', 'F']):
        axs[idx].set_ylabel(name)
    plt.show()


def store_train(df, path):
    """Store subseted scaled dataframe to local

    Args:
        df(pd.Dataframe):obj:`pandas.DataFrame` initial dataset
        path(String): path to store the datafarme

    Returns:
        None

    """
    df.to_csv(path, index=False)
