# dhis2-health-analytics
DHIS2 data for health analytics. We focus on COVID data
 Step 1: use demo covid data from  DHIS2 demo instance at https://play.dhis2.org/demo
 metadata: https://play.dhis2.org/demo/api/metadata 
 Step 2: Use actual covid data 

Sample Data 
https://dhis2.org/downloads/

## set up virtual environment

```
python3 -m venv dhis2
source dhis2/bin/activate

```
Then install the requirements:

```
pip install -r requirements.txt
```

# libs
pip install dhis2.py

## docker
```
docker build -t dhs-app .
docker run -p 8050:8000 --name dhs-app
```

- clear docker cache
```
docker builder prune -f 
```
- on the browser
```
http://localhost:8050
```