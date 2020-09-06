# Coding Excercise
## Provider Utilization and Payment Data

### Provision Medicare Provider Utilization and Payment csv file
Download the [file](https://data.cms.gov/Medicare-Physician-Supplier/Medicare-Provider-Utilization-and-Payment-Data-Phy/fs4p-t5eq/data) and put it on directory of your choice. 
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
```
make up
```
The firt run, sqlite database will be initialized automatically. This will ocurr only once and can take a few minutes.
In any case, sthe start up process will perform the check for CSV and database file integrity. The container should be running in the background when the check completes and the API should be accessible at http://localhost:80. See API Endpoints section below for more details.

### Stop the API container
```
make down
```

## API Endpoints
Refer to http://localhost:80/docs
