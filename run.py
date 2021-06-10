import logging.config
import pandas as pd
import yaml
import argparse
import warnings

from src.clustering import *
from src.get_para import *
from src.get_rec import *

warnings.filterwarnings('ignore')


logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s', level=logging.INFO)
logger = logging.getLogger('run-reproducibility')

if __name__ == '__main__':
    # import data
    data = pd.read_csv("data/sample/final_train_s3.csv")

    parser = argparse.ArgumentParser(description="Acquire, clean, and create features from tic tac toe data")

    parser.add_argument('step', help='Which step to run', choices=['get_para', 'clustering', 'get_rec'])
    parser.add_argument('--input', '-i', default=None, help='Path to input data')
    parser.add_argument('--cluster_num', '-n', default=None, help='Number of clusters')
    parser.add_argument('--config', default='config/test.yaml', help='Path to configuration file')

    args = parser.parse_args()

    with open(args.config, "r") as f:
        config = yaml.load(f)

    logger.info("Configuration file loaded from %s" % args.config)

    if args.input is not None:
        input = pd.read_csv(args.input)
        logger.info('Input data loaded from %s', args.input)

    if args.cluster_num is not None:
        cluster_num = int(args.cluster_num)
        logger.info('Number of clusters loaded as %s', args.cluster_num)

    if args.step == 'get_para':
        subset = subset(data, **config['get_para']['subset'])
        song_filtered = scale(subset, **config['get_para']['scale'])
        song_filtered = song_filtered.dropna()
        mod_list = get_a_mod_list_and_dict(song_filtered, **config['get_para']['get_a_mod_list_and_dict'])
        cluster_selection_plot(song_filtered, mod_list, **config['get_para']['cluster_selection_plot'])
        store_train(song_filtered, **config['get_para']['store_train'])
    elif args.step == 'clustering':
        train_df = load_train(**config['clustering']['load_train'])
        mod_g1_label, df_summary_g1 = quick_result(train_df, final_cluster_num=cluster_num,
                                                   **config['clustering']['quick_result'])
        store_mod_labels(mod_g1_label, **config['clustering']['store_mod_labels'])
    elif args.step == 'get_rec':
        data = load_songs(data, **config['get_rec']['load_songs'])
        labels = load_labels(**config['get_rec']['load_labels'])
        df_song = scale(data, **config['get_rec']['scale'])
        k_songs_z, e_songs_z = get_cluster_df(data, labels, **config['get_rec']['get_cluster_df'])
        merged_df = get_final_rds(k_songs_z, e_songs_z)
        store_rds(merged_df, **config['get_rec']['store_rds'])
