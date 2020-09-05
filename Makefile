# CMS_DIR is going to have the downloaded csv file and sqlite db

#get-data: export CMS_URI=https://data.cms.gov/api/views/fs4p-t5eq/rows.csv?accessType=DOWNLOAD&bom=true&format=true
#get-data: export CMS_EXPECTED_ROWS=9847444
#get-data: export CMS_DIR=$(HOME)/science-data

#get-data:
#	bash scripts/get_data.sh
up: check-env #get-data
	echo ${CMS_DIR}
	echo ${CMS_FILE}
	docker start science-api 2>/dev/null || docker run -d --rm -v ${CMS_DIR}:/science-data -e CMS_DIR=../science-data -e CMS_FILE=${CMS_FILE} --name science-api -p 80:80 arllanos/science-api
	docker exec -it science-api python3 scripts/csv2db.py

down:
	docker kill science-api 2>/dev/null || true

check-env:
ifndef CMS_DIR
	$(error CMS_DIR is undefined. Define using: export CMS_DIR=<csv_directory>)
endif
ifndef CMS_FILE
	$(error CMS_FILE is undefined. Define using: export CMS_FILE=<csv_file_name>)
endif
