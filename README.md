# Coding Excercise
## Provider Utilization and Payment Data

### Provision Medicare Provider Utilization and Payment csv file
Download the [file](https://data.cms.gov/Medicare-Physician-Supplier/Medicare-Provider-Utilization-and-Payment-) and put it on directory of your choice. 
Then set the following variables accordingly:
```
export CMS_DIR=<csv_directory>
export CMS_FILE=<csv_file_name>
```
Example values:
```
export CMS_DIR=$HOME/science-data
export CMS_FILE=mpup.csv
```

### Start the API container
The firt run, sqlite database will be initialized automatically.
This will ocurr only once but would takes a few minutes.
```
make up
```
While the API container is runnning it is accessible through http://localhost:80. See API Endpoints section below for more details.

### Stop the API container
```
make down
```

## API Endpoints
Refer to http://localhost:80/docs
