# location and name of csv data
CMS_DIR := $(HOME)/science-data
CMS_FILE := cms.csv

init: export CMS_EXPECTED_ROWS=9847444
init: export CMS_DIR=$(HOME)/science-data
init: export CMS_FILE=cms.csv

init: up
	bash scripts/get_data.sh
	docker exec -it science-api python3 scripts/csv2db.py

up:
	docker start science-api 2>/dev/null || docker run -d --rm -v $(CMS_DIR):/science-data -e CMS_DIR=../science-data -e CMS_FILE=$(CMS_FILE) --name science-api -p 80:80 arllanos/science-api

down:
	docker kill science-api 2>/dev/null || true