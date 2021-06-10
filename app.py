import traceback
import logging.config
from flask import Flask
from flask import render_template, request, redirect, url_for
import numpy as np

# Initialize the Flask application
app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

# Configure flask app from flask_config.py
app.config.from_pyfile('config/flaskconfig.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])
logger.debug('Web app log')

# Initialize the database session
from src.add_songs import Tracks, TrackManager
print(app)
track_manager = TrackManager(app)

@app.route('/')
def index():
    """Main view that lists songs in the database.

    Create view into index page that uses data queried from Track database and
    inserts it into the msiapp/templates/index.html template.

    Returns: rendered html template

    """

    try:
        #tracks = track_manager.session.query(Tracks).limit(app.config["MAX_ROWS_SHOW"]).all()
        tracks = track_manager.session.query(Tracks).all()
        artist_list = []
        for t in tracks:
            if t.artist=="taylor":
                artist_list.append("Taylor Swift")
            else:
                artist_list.append(t.artist)
        artist_list = np.unique(np.array(artist_list)).tolist()
        logger.debug("Index page accessed")
        return render_template('index.html', tracks=tracks, artist_list = artist_list)
    except:
        traceback.print_exc()
        logger.warning("Not able to display tracks, error page returned")
        return render_template('error.html')


@app.route('/add', methods=['POST'])
def add_entry():
    """View that process a POST with new song input

    :return: redirect to index page
    """

    try:
        print(request.form)
        track_manager.add_track(title = request.form["title"], artist=request.form['artist'], closest_k_song=request.form['k_pop_song'], closest_k_artist=request.form['k_pop_artist'])
        logger.info("New song added: %s by %s", request.form['title'], request.form['artist'],request.form['k_pop_song'],request.form['k_pop_artist'] )
        return redirect(url_for('index'))
    except:
        logger.warning("Not able to display tracks, error page returned")
        return render_template('error.html')

@app.route('/get', methods=['POST'])
def get_recommend():
    """Get recommendatioon from new song input

    :return: redirect to index page
    """

    try:
        artist = request.form['artist']
        title = request.form["title"]
        rec = track_manager.session.query(Tracks).filter(Tracks.title==title, Tracks.artist==artist).all()
        #rec = track_manager.session.query(Tracks).limit(1).all()
        k_song = rec[0].closest_k_song
        k_artist = rec[0].closest_k_artist
        logger.info("Get song recommendation: %s by %s", k_song, k_artist)
        return render_template('rec.html',k_song = k_song,k_artist=k_artist )
    except:
        logger.warning("Not able to get tracks, error page returned")
        return render_template('error.html')

@app.route('/songs', methods=['POST'])
def get_songs():
    """Get recommendatioon from new song input

    :return: redirect to index page
    """

    try:
        artist = request.form.get('artist_list')
        if artist == "Taylor Swift":
            artist = "taylor"
        songs = track_manager.session.query(Tracks).filter(Tracks.artist==artist).all()
        titles = []
        for t in songs:
            titles.append(t.title)
        titles = np.unique(np.array(titles)).tolist()
        logger.info("Get songs by %s", artist)
        if artist == "taylor":
            artist = "Taylor Swift"
        return render_template('songs.html',artist_name = [artist],artist_header =artist ,song_name = titles)
    except:
        logger.warning("Not able to get tracks, error page returned")
        return render_template('error.html')

@app.route('/get_2', methods=['POST'])
def get_recommend_2():
    """Get recommendatioon from new song input

    :return: redirect to index page
    """

    try:
        artist = request.form.get('artist_name')
        if artist == "Taylor Swift":
            artist = "taylor"
        title = request.form.get('song_name')
        rec = track_manager.session.query(Tracks).filter(Tracks.title==title, Tracks.artist==artist).all()
        k_song = rec[0].closest_k_song
        k_artist = rec[0].closest_k_artist[:-2].upper()
        logger.info("Get song recommendation: %s by %s", k_song, k_artist)
        link = "https://www.youtube.com/results?search_query="+k_artist.replace(" ","+")+"+"+k_song.replace(" ","+")
        print(link)
        return render_template('rec.html',k_song = k_song,k_artist=k_artist,link=link)
    except:
        logger.warning("Not able to get tracks, error page returned")
        return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
