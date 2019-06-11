# ACME
ACME is python flask back end application to upload large CSV file and render data with pagination.

## Start Application
```bash
python manage.py runserver
```

## Install
Install following dependencies for the application.
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo apt-get install libpq-dev
sudo apt-get install redis-server
```

## Start Redis

To start async file uploading feature.
Right now, the application is not using async frameworks like celery or dramatiq. But will need redis for queue management. 

```bash
sudo systemctl enable redis-server.service
sudo systemctl start redis-server.service
```
### Starting Dramatiq worker
```bash
 env PYTHONPATH=. dramatiq uploadFileTask
```


## Prepare Database

```bash
python manage.py db init
python manage.py migrate
python manage.py upgrade
```
