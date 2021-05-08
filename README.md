# MSiA423 Kpop Recommender 

Author: Qiaozhen Wu \
QA: Sherman Lu

<!-- toc -->

## Project Charter 
![](figures/kpop.jpg)

#### Vision:

With the rise of popularity of Korean pop music (K-Pop) around the world, the global music scene is witnessing a shift from the previously western-dominating industry to a more diverse market with non-English songs. Music is a form of communication capable of surpassing language and cultural differences, allowing people from various cultural backgrounds to experience arts from other cultures in the most authentic ways. The music industries in the US and Korea maintain substantially different standards, but they share similarities in the common emotions songs convey and in the genres of music. Therefore, what one likes to listen to among English songs might be a good indicator of their taste for Korean songs as well. With the help of my app, users would receive recommendation of Korean songs regarding their preference among western music. The app would hopefully introduce K-pop to more people, reduce prejudice and stereotypes on the east in western countries and thus help break cultural barriers. 

#### Mission:

Users would input three of their favorite western songs/artists, and the app would output a recommendation of three Korean songs/artist that might suit the users’ tastes. The app will use dataset from the Spotify Web API (https://developer.spotify.com/documentation/web-api/) for 200 Korean songs and 200 English songs, and also a dataset that aggregates the former one to the level of each artist. The numerical metric of each songs includes values like “speechless”, “danceability”, “energy” and “acousticness”, which Spotify uses to evaluate each song. The model will be using KNN model that calculates the distance between the inputed songs/artist and output their “closest” Korean counter parts. If time permits, I will also experiment on a feature that document the lyrics and themes of each songs, which potentially would be a significant indicator of the user’s taste apart from the metrics of Spotify.

#### Success Criteria:

To test the performance of the model, I will collect playlists of users who listens to both English and Korean songs scraped from twitter, and calculate the true positive rate of the recommender. The recommender will be deployed if the true positive rate reaches 0.7. To determine the business success of my app among users, standard A/B testing will be used to evaluate whether users like the recommended songs based on their ratings, by randomly assign half of the users to randomly generated recommendation. Overall, the app would introduce Korean songs to the users that might be hearing it for the first time, and provide them with a novel while enjoyable music experience. 

- [Directory structure](#directory-structure)
- [Data Aquisition](#Data-Aquisition)
- [Create Docker Image](#2-Create-Docker-Image)
- [How to upload/Download data on S3](#3-How-to-upload/Download-data-on-S3)
  * [1. Set up AWS credential in your environment](#Set-up-AWS-credential-in-your-environment)
  * [Upload data to S3 from local](#Upload-data-to-S3-from-local)
  * [Download data to local from S3](#Download-data-to-local-from-S3)
- [Running the app in Docker](#running-the-app-in-docker)
  * [Initialize the database](#Initialize-the-database)
    * [Create the database](#Creat-the-database)
    * [Adding songs](#Adding-songs)
    * [Defining your engine string](#Defining-your-engine-string)
    * [Local SQLite database](#Local-SQLite-database)
  * [Connecting to remote databases](#Connecting-to-remote-databases)
    * [Requirements](#Requirements)
    * [1. Connecting to MYSQL](#1-Connecting-to-MYSQL)
    * [2. Create database with docker image](#2-Create-database-with-docker-image)
    * [3. Ingest data into database with docker image](#3-Ingest-data-into-database-with-docker-image)

<!-- tocstop -->

## Directory structure 

```
├── README.md                         <- You are here
├── api
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── boot.sh                       <- Start up script for launching app in Docker container.
│   ├── Dockerfile                    <- Dockerfile for building image to run app  
│
├── config                            <- Directory for configuration files 
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
│   ├── logging/                      <- Configuration of python loggers
│   ├── flaskconfig.py                <- Configurations for Flask API 
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── external/                     <- External data sources, usually reference data,  will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│
├── docs/                             <- Sphinx documentation based on Python docstrings. Optional for this project. 
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── deliver/                      <- Notebooks shared with others / in final state
│   ├── develop/                      <- Current notebooks being used in development.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports, helper functions, and SQLAlchemy setup. 
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source data for the project 
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
│
├── app.py                            <- Flask wrapper for running the model 
├── run.py                            <- Simplifies the execution of one or more of the src scripts  
├── requirements.txt                  <- Python package dependencies 
```

## Data Aquisition

To aquire the data, download the dataset from this [link](https://www.kaggle.com/qiaozhenwu/kpopwesternsongs). You can also find the dataset in the data/sample/ folder.

## Create Docker Image

Use the following command to create the docker image kpop-recommender:
```
docker build -f Dockerfile_data -t kpop_recommender .
```
## How to upload/Download data on S3


#### Set up AWS credential in your environment 

To get access to S3, you need two environment variables for your secret keys to AWS:AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.You would be able to get these
values from yor AWS S3 console, and run the following command to export them to your enviroment.
```
export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_ACCESS_KEY"
```

#### Upload data to S3 from local 

After seting up the AWS credential, to upload data to S3 from local, use the following command. The defualt of local_path
is 'data/sample/final_train_s3.csv'. And the default of s3_path is 's3://2021-msia423-wu-qiaozhen/kpop_recommender_s3.csv'.
```
python src/s3.py --local_path={your_local_path} --s3_path={your_s3_path}
```

#### Download data to local from S3 
To upload data to S3 from local, use the following command, using the same default value as above:
```
 python src/s3.py --download --local_path={your_local_path} --s3_path={your_s3_path}
```

## Database
### 1. Initialize the database 

#### Create the database 
To create the database in the location configured in `config.py` run: 

`python run.py create_db --engine_string=<engine_string>`

By default, `python run.py create_db` creates a database at `sqlite:///data/tracks.db`.

#### Adding songs 
To add songs to the database:

`python run.py ingest --engine_string=<engine_string> --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`

By default, `python run.py ingest` adds *Minor Cause* by Emancipator to the SQLite database located in `sqlite:///data/tracks.db`.

#### Defining your engine string 
A SQLAlchemy database connection is defined by a string with the following format:

`dialect+driver://username:password@host:port/database`

The `+dialect` is optional and if not provided, a default is used. For a more detailed description of what `dialect` and `driver` are and how a connection is made, you can see the documentation [here](https://docs.sqlalchemy.org/en/13/core/engines.html). We will cover SQLAlchemy and connection strings in the SQLAlchemy lab session on 
#### Local SQLite database 

A local SQLite database can be created for development and local testing. It does not require a username or password and replaces the host and port with the path to the database file: 

```python
engine_string='sqlite:///data/kpop_recommender.db'
```

The three `///` denote that it is a relative path to where the code is being run (which is from the root of this directory).

You can also define the absolute path with four `////`, for example:

```python
engine_string = 'sqlite://///Users/Desktop/MSIAHW/423/2021-msia423-Wu-Qiaozhen-project/data/kpop_recommender.db'
```
### 2. Connecting to remote databases 

##### Requirements 
To successfully connect to the remote databases, you need too:

1. Connect to the Northwestern VPN. 
   

2. Build the kpop_recommender image built as described in the [Docker Image section].
   

3. You need to set up the following environment variables from building your 
AWS credential section. Note please replace the section within and including the "".
```
   export MYSQL_USER="YOUR_SQL_USER_NAME"
   export MYSQL_PASSWORD="YOUR_SQL_PASSWORD"
   export MYSQL_HOST="YOUR_SQL_HOST"
   export MYSQL_PORT="YOUR_SQL_PORT"
   export DATABASE_NAME="YOUR_DATABASE_NAME"
```

##### 1. Connecting to MYSQL

To connect to your MYSQL database, run the following command:

```
docker run -it --rm mysql:5.7.33 mysql -h$MYSQL_HOST -u$MYSQL_USER -p$MYSQL_PASSWORD
```
If you succeeded, you will enter the interactive mysql session. To view your tables, use the commands:\
show databases; use {database name}; show tables;

##### 2. Create database with docker image

To create a new databases, use the the following command. The script specifies the engine string in config/flaskconfig.py.
```
docker run -it -e MYSQL_HOST -e MYSQL_PORT -e MYSQL_USER -e MYSQL_PASSWORD -e DATABASE_NAME kpop_recommender run.py create_db --engine_string=={your_engine_string}
```

##### 3. Ingest data into database with docker image
Your can also ingest data through the following command. If you don't specify the parameters "artist","album","title," the default would "bts","BE","Dis-ease" respectively.
```
docker run -it -e MYSQL_HOST -e MYSQL_PORT -e MYSQL_USER -e MYSQL_PASSWORD -e DATABASE_NAME kpop_recommender run.py ingest --artist={your_artist} --album={your_album} --title ={your_song_title}
```



 
