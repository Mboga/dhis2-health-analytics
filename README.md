
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

## deploy on gcp
- set up gcp authentication
```
 gcloud auth login
```
- List all gcloud projects list
```
gcloud projects list

```

- Set the default project for your gcloud CLI session

```
 gcloud config set project your_project_id

 ```
For example:
```
 gcloud config set project api-project-507320880300

 ```

- use Cloud build to build your image and push it to google containers registry in one step

```
gcloud builds submit --tag gcr.io/api-project-507320880300/dhs-app:latest .

```


- run the app

```
gcloud run deploy dhs-app-service \
    --image gcr.io/api-project-507320880300/dhs-app:latest \
    --region europe-west1 \
    --platform managed \
    --allow-unauthenticated \
    --port 8000 \
    --project api-project-507320880300

```

success !
The app will be live in the url:
```
https://dhs-app-service-507320880300.europe-west1.run.app

```

