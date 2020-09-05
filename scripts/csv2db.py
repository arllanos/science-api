import os
import numpy as numpy
import pandas as pd
import sqlite3
from sqlalchemy import create_engine
from time import perf_counter as pc

DIR = os.environ['CMS_DIR']
FILE_CSV = os.environ['CMS_FILE']
FILE_DB = os.path.splitext(FILE_CSV)[0]

csv_fullpath = '{}/{}'.format(DIR, FILE_CSV)
csv_base = os.path.basename(csv_fullpath)
db_base = '{}.{}'.format(os.path.splitext(csv_base)[0], 'db')
db_fullpath = '{}/{}'.format(DIR, db_base)

try:
    num_lines = sum(1 for line in open(csv_fullpath))
    print('About to import {} records to sqlite'.format(num_lines))
except FileNotFoundError:
    print('Input CSV file not found.')

if os.path.isfile(db_fullpath):
    print('{} file found. Will re-import.'.format(db_fullpath))
    os.remove(db_fullpath)

SQLALCHEMY_DATABASE_URL='sqlite:///{}'.format(db_fullpath)

conn = create_engine(SQLALCHEMY_DATABASE_URL)

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
print('Done. Elapsed time(s) {}               '.format(elapsed))

df = pd.read_sql_query('select count(*) as cnt from mytable', conn)

print('Num rows in csv w/o header .: ', num_lines-1)
print('Num rows in sqlite..........: ', df['cnt'][0])
