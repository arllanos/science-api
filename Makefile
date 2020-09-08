up: check-env
	docker start science-api 2>/dev/null || docker run -d --rm -v ${CMS_DIR}:/science-data -e CMS_DIR=../science-data -e CMS_FILE=${CMS_FILE} --name science-api -p 80:80 arllanos/science-api
	docker exec -it science-api python3 csv2db.py

down:
	docker kill science-api 2>/dev/null || true

check-env:
ifndef CMS_DIR
	$(error CMS_DIR is undefined. Define using: export CMS_DIR=<csv_directory>)
endif
ifndef CMS_FILE
	$(error CMS_FILE is undefined. Define using: export CMS_FILE=<csv_file_name>)
endif
