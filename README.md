
## dhis2-health analytics

A dash web application to visualise dhis2 data.

Sample Data for Sierra Leone is downloaded from the dhis2 link: https://dhis2.org/downloads/

## local set up

```
python3 -m venv dhis2
source dhis2/bin/activate

```
Then install the requirements:

```
pip install -r requirements.txt
```

To launch the app:
```
python src/app.py
```

## docker

- clear docker cache
```
docker builder prune -f 
```
- Build the docker image

```
docker build -t dhs-app .
docker run -p 8050:8000 --name dhs-app
```

- on the browser
```
http://localhost:8050
```

## deploy on azure


## deploy on aws


## deploy on gcp




