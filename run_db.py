import argparse
import pandas as pd

import logging.config
logging.config.fileConfig('config/logging/local.conf')
logger = logging.getLogger('kpop-recommender-pipeline')

from src.add_songs import TrackManager, create_db
from config.flaskconfig import SQLALCHEMY_DATABASE_URI

if __name__ == '__main__':

    # Add parsers for both creating a database and adding songs to it
    parser = argparse.ArgumentParser(description="Create and/or add data to database")
    subparsers = parser.add_subparsers(dest='subparser_name')

    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create_db", description="Create database")
    sb_create.add_argument("--engine_string", default=SQLALCHEMY_DATABASE_URI,
                           help="SQLAlchemy connection URI for database")

    # Sub-parser for ingesting new data
    sb_ingest = subparsers.add_parser("ingest", description="Add data to database")
    sb_ingest.add_argument("--artist", default="bts", help="Artist of song to be added")
    sb_ingest.add_argument("--title", default="Dis-ease", help="Title of song to be added")
    sb_ingest.add_argument("--k_artist", default="bts", help="Artist of song being added")
    sb_ingest.add_argument("--k_title", default="BE", help="Title of song being added")
    sb_ingest.add_argument("--engine_string", default=SQLALCHEMY_DATABASE_URI,
                           help="SQLAlchemy connection URI for database")

    # Sub-parser for loading the entire dataset
    sb_load = subparsers.add_parser("load_rds", description="Add dataset to database")
    sb_load.add_argument("--load_path", default="data/sample/rds.csv", help="Artist of song to be added")
    sb_load.add_argument("--engine_string", default=SQLALCHEMY_DATABASE_URI,
                       help="SQLAlchemy connection URI for database")

    args = parser.parse_args()
    sp_used = args.subparser_name
    if sp_used == 'create_db':
        create_db(args.engine_string)
    elif sp_used == 'ingest':
        tm = TrackManager(engine_string=args.engine_string)
        tm.add_track(args.title, args.artist, args.k_title, args.k_artist)
        tm.close()
    elif sp_used == 'load_rds':
        songs = pd.read_csv(args.load_path)
        tm = TrackManager(engine_string=args.engine_string)
        for i in range(0,songs.shape[0]):
            song = songs.iloc[i]
            tm.add_track(song["track_name_x"],song["artist_x"],song["track_name_y"],song["artist_y"])
        tm.close()

    else:
        parser.print_help()



