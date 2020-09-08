# Coding Excercise
## Provider Utilization and Payment Data
This is a minimalist REST API to obtain basic stats about the Provider Utilization and Payment dataset.

### Provision Medicare Provider Utilization and Payment csv file
Download the data [file](https://data.cms.gov/Medicare-Physician-Supplier/Medicare-Provider-Utilization-and-Payment-Data-Phy/fs4p-t5eq/data) and put it on a directory of your choice. 
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
In any case, the start up process will perform the check for CSV and database file integrity. 
After db initialization or db integrity check, the container should be running in the background and the API should be accessible at http://localhost:80. See API Endpoints section below for more details.
To check the container is up and running run:
```
docker ps -a
```

### Stop the API container
```
make down
```

## API Endpoints
Refer to http://localhost:80/docs

### Get Stats for a metric

**GET** `http://localhost:80/stats/metric/<metric>?<list_of_filter_as_key_value_pairs>`

| Code | Description  |
| ---- | ------------ |
| 200  | OK |
| 400  | Not found |
| 500  | Server error |

**Example Request**

![alt text](https://gist.githubusercontent.com/arllanos/ade072aa76cf53c358ed8504b62a460f/raw/9650017aaaad6e4e3fa3c0cea884a68a48ca99a9/science-api-gist.JPG "Stats request")

```
curl -X GET "http://localhost:8000/stats/metric/NumberofServices?filters=%7B%22CountryCodeoftheProvider%22%3A%20%22US%22%7D&filters=%7B%22ZipCodeoftheProvider%22%3A%20602011718%7D&filters=%22HCPCSCode%22%3A%2099232" -H  "accept: application/json"
```

**Example Response**
```json
Code: 200
{
  "min": 12,
  "max": 2307,
  "mean": 211.0493827160494
}
```
