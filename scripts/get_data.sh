if [ -z "$CMS_DIR" ]; then
    echo "\$CMS_DIR is empty. Initialize using: export CMS_DIR=\$HOME/science-data"
    exit 1
fi

if [ -z "$CMS_URI" ]; then
    echo "\$CMS_URI is empty. Initialize using: export CMS_URI=<uri_to_cvs_data>"
    exit 1
fi


if [ -z "$CMS_EXPECTED_ROWS" ]; then
    echo "\$CMS_URI is empty. Initialize using: export CMS_EXPECTED_ROWS=<expected_num_of_rows_with_header>"
    exit 1
fi

mkdir -p $CMS_DIR && chmod +w $CMS_DIR

FILE=$CMS_DIR/cms.csv
if [ -f $FILE ]; then
    CMS_ACTUAL_ROWS=`wc -l < $FILE`
    if [ $CMS_ACTUAL_ROWS -eq $CMS_EXPECTED_ROWS ]; then
        echo "Data already downloaded looks OK. Skiping download."
        exit
    else
        echo "File on disk has $CMS_ACTUAL_ROWS rows but $CMS_EXPECTED_ROWS rows are expected"
    fi
fi

echo "Will download from $CMS_URI to $FILE"

wget -c $CMS_URI -O $FILE
