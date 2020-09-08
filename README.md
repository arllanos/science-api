# Coding Excercise
## Provider Utilization and Payment Data
This is a minimalist REST API to obtain basic stats about the Provider Utilization and Payment dataset.

## Running the application
### 1. Provision Medicare Provider Utilization and Payment csv file
Download the data [file](https://data.cms.gov/Medicare-Physician-Supplier/Medicare-Provider-Utilization-and-Payment-Data-Phy/fs4p-t5eq/data) and put it on a directory of your choice. 
Then set the following variables accordingly:
```bash
export CMS_DIR=<csv_directory>
export CMS_FILE=<csv_file_name>
```
Example values:
```bash
export CMS_DIR=$HOME/science-data
export CMS_FILE=mpup.csv
```

### 2. Initialize the database
```bash
make up
```
Wait a few seconds to make sure the service is running and then run:
```bash
rm -f ${CMS_DIR}/$(echo ${CMS_FILE%%.*}.db) && docker exec -it science-api python3 csv2db.py
```
### 3. Start the service and stop the service
To start the service:
```
make up
```
To check if the container is up and running:
```bash
docker ps -a
```
The container should be running in the background and the API should be accessible at http://localhost:80. See API Endpoints section below for more details.

To stop the container:

```bash
make down
```

## API Endpoints
Refer to http://localhost:80/docs

### Get Stats for a metric
#### Notes
Metric names (numerical columns) as well as filter names (categorical columns) follows the same names as the official dataset except that blank spaces as well as special caracters like "/" are removed.

**Region related values to use as filters (categorical)**: CountryCodeoftheProvider, StateCodeoftheProvider, CityoftheProvider, ZipCodeoftheProvider, HCPCSCode

**Numerical columns to compute stats**: NumberofServices, NumberofMedicareBeneficiaries, NumberofDistinctMedicareBeneficiaryPerDayServices, AverageMedicareAllowedAmount, AverageSubmittedChargeAmount, AverageMedicarePaymentAmount, AverageMedicareStandardizedAmount

**GET** `http://localhost:80/stats/metric/<metric_id>?<list_of_filter_as_key_value_pairs>`

| Code | Description  |
| ---- | ------------ |
| 200  | OK |
| 400  | Not found |
| 500  | Server error |

**Example Request**

![alt text](https://gist.githubusercontent.com/arllanos/ade072aa76cf53c358ed8504b62a460f/raw/9650017aaaad6e4e3fa3c0cea884a68a48ca99a9/science-api-gist.JPG "Stats request")

| Name | Description  |
| ---- | ------------ |
| metric_id  | NumberofServices |
| filters  | {"CountryCodeoftheProvider": "US"} |
|   | {"ZipCodeoftheProvider": 602011718} |
|   | {"HCPCSCode": 99232} |

```
curl -X GET "http://localhost:8000/stats/metric/NumberofServices?filters=%7B%22CountryCodeoftheProvider%22%3A%20%22US%22%7D&filters=%7B%22ZipCodeoftheProvider%22%3A%20602011718%7D&filters=%7B%22HCPCSCode%22%3A%2099232%7D" -H  "accept: application/json"
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
