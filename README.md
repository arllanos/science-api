# Coding Excercise
## Provider Utilization and Payment Data

## REST API functional requirements
- Answer active questions like:
    - cost per region
    - cost accross regions
    - treatment level (length of visits, in-patient, out-patient)
- Provide basic statistics for the data
    - TBD

## Build docker image
```bash
# initialize variables
DOCKER_REGISTRY=docker.io
DOCKER_USER=arllanos
INSTALL_JUPYTER=true # set to false if do not need to enable data exploration
docker build --build-arg INSTALL_JUPYTER=true -t $DOCKER_REGISTRY/$DOCKER_USER/science-api .
```

## Download data
```
HOST_DATA_DIR=$HOME/science-data
mkdir -p $HOST_DATA_DIR
wget -c https://data.cms.gov/api/views/fs4p-t5eq/rows.csv?accessType=DOWNLOAD -O $HOST_DATA_DIR/cms.csv
```

## Start API docker container
```
docker run --rm -d -v $HOST_DATA_DIR:/science-data --name science-api -p 80:80 arllanos/science-api
```
## Start Jupyter docker container
```
docker run --rm -ti -v $HOST_DATA_DIR:/app/science-data --name science-jupyter -p 8888:8888 arllanos/science-api jupyter lab --ip=0.0.0.0 --allow-root --NotebookApp.custom_display_url=http://127.0.0.1:8888
```