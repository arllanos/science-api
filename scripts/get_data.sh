if [ -z "$CMS_DIR" ];then
    echo "\$CMS_DIR is empty. Initialize using: export CMS_DIR=\$HOME/science-data"
    exit 1
fi

if [ -z "$CMS_FILE" ];then
    echo "\$CMS_FILE is empty. Initialize using: export CMS_FILE=cms.csv"
    exit 1
fi

if [ -z "$CMS_EXPECTED_ROWS" ];then
    CMS_EXPECTED_ROWS=9847444
fi

data=$CMS_DIR/$CMS_FILE
if [ `wc -l < $data` -eq $CMS_EXPECTED_ROWS ];then 
    echo "Data already downloaded looks OK. Skiping download."
    exit
fi

mkdir -p $CMS_DIR
wget -c https://data.cms.gov/api/views/fs4p-t5eq/rows.csv?accessType=DOWNLOAD -O $data