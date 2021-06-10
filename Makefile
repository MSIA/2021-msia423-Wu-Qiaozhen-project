.PHONY: image raw cloud_table feature_table rf_model test test-local all

CONFIG_FILE = config/test.yaml

image_data:
	docker build -f Dockerfile -t kpop_recommender .

image_app:
	docker build -f app/Dockerfile -t kpop_recommender_app .

docker_clean_im:
	docker image prune

docker_clean_container:
	docker rm $(docker ps --filter status=exited -q)

# Database
.PHONY: mysql_it create_db ingest_db load_db

mysql_it:
	docker run -it --rm \
		mysql:5.7.33 \
		mysql \
		-h$$MYSQL_HOST \
		-u$$MYSQL_USER \
		-p$$MYSQL_PASSWORD

create_db:
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ \
		-e SQLALCHEMY_DATABASE_URI \
		kpop_recommender run_db.py create_db

load_db:
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ \
		-e SQLALCHEMY_DATABASE_URI \
		kpop_recommender run_db.py load_rds --load_path "data/sample/run_rds.csv"

.PHONY: s3_upload, s3_download, get_para, clustering, get_rec, model_all

s3_upload:
	docker run \
		-e AWS_ACCESS_KEY_ID \
		-e AWS_SECRET_ACCESS_KEY \
		kpop_recommender run_s3.py

data/sample/final_train_s3.csv: run_s3.py
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ \
		-e AWS_ACCESS_KEY_ID \
		-e AWS_SECRET_ACCESS_KEY \
		kpop_recommender run_s3.py --download

s3_download: data/sample/final_train_s3.csv

data/sample/run_rds.csv: data/sample/final_train_s3.csv run.py
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ kpop_recommender run.py get_para

get_para: data/sample/run_rds.csv

data/run/mod_labels.csv:data/run/mod_labels.csv run.py
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ kpop_recommender run.py clustering --cluster_num 8

clustering: data/run/mod_labels.csv

data/sample/run_rds.csv: data/run/mod_labels.csv run.py
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ kpop_recommender run.py get_rec

get_rec: data/sample/run_rds.csv

model_all: s3_download get_para clustering get_rec

# App
.PHONY: docker-app-local kill-app-local

run_app_local:
	docker run -e SQLALCHEMY_DATABASE_URI \
		-p 5000:5000 --name test kpop_recommender_app

kill_app_local:
	docker kill test

# Test
pytest:
	docker run kpop_recommender -m pytest

# Theory of Everything
.PHONY: all_in_one

all_in_one: model_all create-db load_db run_app_local