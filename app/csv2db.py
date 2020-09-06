import os
import numpy as numpy
import pandas as pd
import sqlite3
import sys
from sqlalchemy import create_engine
from time import perf_counter as pc
from database import engine, db_fullpath, csv_fullpath

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
    print('Num rows in Sqlite..........: ', rows_db)

def main():
    # read csv file
    try:
        num_lines = sum(1 for line in open(csv_fullpath))
        print('Found CSV file'.format(num_lines))
    except FileNotFoundError:
        print('Input CSV file not found.')

    # read db if already initialized
    if os.path.isfile(db_fullpath):
        print('Found Sqlite db')
        df = pd.read_sql_query('select count(*) as cnt from mytable', engine)
        num_rows = df['cnt'][0]
        
        print_summary(num_lines-1, num_rows)

        if num_lines-1 != num_rows:
            print('Sqlite needs re-import.')
            os.remove(db_fullpath)
        else:
            return
    else:
        print('Sqlite db file not found. Will initialize new db file...')

    # import the data
    num_rows = import_data(engine)

    print_summary(num_lines-1, num_rows)

if __name__ == '__main__':
    main()
