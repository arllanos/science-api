import os
import numpy as numpy
import pandas as pd
import sqlite3
import sys
from sqlalchemy import create_engine
from time import perf_counter as pc

DIR = os.environ['CMS_DIR']
FILE_CSV = os.environ['CMS_FILE']
FILE_DB = os.path.splitext(FILE_CSV)[0]

csv_fullpath = '{}/{}'.format(DIR, FILE_CSV)
csv_base = os.path.basename(csv_fullpath)
db_base = '{}.{}'.format(os.path.splitext(csv_base)[0], 'db')
db_fullpath = '{}/{}'.format(DIR, db_base)

def import_data(conn):
    chunksize = 10000
    j = 0
    t0 = pc()

    for df in pd.read_csv(csv_fullpath, chunksize=chunksize, iterator=True):
        df = df.rename(columns = {c: c.replace(' ', '') for c in df.columns})
        df = df.rename(columns = {c: c.replace('/', '') for c in df.columns})
        df.index += j

        df.to_sql('mytable', conn, if_exists = 'append')
        j = df.index[-1]+1

        elapsed = pc() - t0
        print('| index: {}. Elapsed time(s) {}'.format(j, elapsed), sep=' ', end='\r')
    elapsed = pc() - t0
    print('Done. Elapsed time(s) {}       '.format(elapsed))

    df = pd.read_sql_query('select count(*) as cnt from mytable', conn)

    num_rows = df['cnt'][0]
    return num_rows

def print_summary(rows_csv, rows_db):
    print('Num rows in csv w/o header .: ', rows_csv)
    print('Num rows in sqlite..........: ', rows_db)

def main():
    # read csv file
    try:
        num_lines = sum(1 for line in open(csv_fullpath))
        print('Found CSV file'.format(num_lines))
    except FileNotFoundError:
        print('Input CSV file not found.')

    # read db if already initialized
    if os.path.isfile(db_fullpath):
        print('Found sqlite db')
        SQLALCHEMY_DATABASE_URL='sqlite:///{}'.format(db_fullpath)
        conn = create_engine(SQLALCHEMY_DATABASE_URL)
        df = pd.read_sql_query('select count(*) as cnt from mytable', conn)
        num_rows = df['cnt'][0]
        
        print_summary(num_lines-1, num_rows)

        if num_lines-1 != num_rows:
            print('SQLITE needs re-import.')
            os.remove(db_fullpath)
        else:
            return
    else:
        print('sqlite db file not found. Will initialize new db file...')

    SQLALCHEMY_DATABASE_URL='sqlite:///{}'.format(db_fullpath)
    conn = create_engine(SQLALCHEMY_DATABASE_URL)

    # import the data
    num_rows = import_data(conn)

    print_summary(num_lines-1, num_rows)

if __name__ == '__main__':
    main()
