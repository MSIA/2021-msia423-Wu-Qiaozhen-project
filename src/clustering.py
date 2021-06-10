import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans


def load_train(path):
    """load subsetted scaled dataframe to local

    Args:
        df(pd.Dataframe):obj:`pandas.DataFrame` initial dataset
        path(String): path to load the datafarme

    Returns:
        df (:obj:`pandas.DataFrame`): loaded dataframe
    """
    df = pd.read_csv(path)
    return df

#used for plotting, so there's no testing for this
def summary_kmeans(df, mod, grand_mean):
    """produce kmeans summary and F score

    Args:
        df(pd.Dataframe):obj:`pandas.DataFrame` initial dataset
        mod(KMeans):obj: input kmeans mod
        grand_mean(List): means for the original dataframe

    Returns:
        df(pd.Dataframe):obj:`pandas.DataFrame` dataframe of cluster centers
        F(double): F score

    """
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
def summary_plot(df, mod_num, seed):
    """produce plot of clusters for specific number of mod

    Args:
        df(pd.Dataframe):obj:`pandas.DataFrame` initial dataset
        mod_num(int):obj: input number of clusters
        seed(int): set seed for the kmeans model

    Returns:
        None

    """
    grand_mean = df.mean(axis=0).values
    mod = KMeans(n_clusters=mod_num, random_state=seed).fit(df)
    df_summary, _ = summary_kmeans(df, mod, grand_mean)
    fig, axs = plt.subplots(nrows=1, ncols=mod.n_clusters, figsize=(25, 5))
    for i in range(mod.n_clusters):
        if i > 0:
            axs[i].get_yaxis().set_ticklabels([])
        axs[i].scatter(x=df_summary.iloc[i, 2:].values, y=list(df.columns), color='royalblue')
        axs[i].set_xlabel(f'cluster{str(i)}')
    plt.show()


def quick_result(df, final_cluster_num, seed):
    """produce cluster labels and cluster centers

    Args:
        df(pd.Dataframe):obj:`pandas.DataFrame` initial dataset
        final_cluster_num(int):obj: input number of clusters
        seed(int): set seed for the kmeans model

    Returns:
        mod.labels_(List): list of labels for each row of the dataframe
        df_summary(pd.Dataframe):obj:`pandas.DataFrame`: dataframe of cluster centers

    """
    grand_mean = df.mean(axis=0).values
    mod = KMeans(n_clusters=final_cluster_num, random_state=seed).fit(df)
    df_summary, _ = summary_kmeans(df, mod, grand_mean)
    summary_plot(df, final_cluster_num, seed)
    return mod.labels_, df_summary


def store_mod_labels(mod_label, path):
    """Store cluster labels to local csv

    Args:
        mod_label(np.array): numpy array of all cluster labels
        path(String): path to store the labels

    Returns:
        None

    """
    np.savetxt(path, mod_label)
