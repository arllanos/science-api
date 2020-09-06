import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DIR = os.environ['CMS_DIR']
FILE_CSV = os.environ['CMS_FILE']

csv_fullpath = '{}/{}'.format(DIR, FILE_CSV)
csv_base = os.path.basename(csv_fullpath)
db_base = '{}.{}'.format(os.path.splitext(csv_base)[0], 'db')
db_fullpath = '{}/{}'.format(DIR, db_base)

SQLALCHEMY_DATABASE_URL='sqlite:///{}'.format(db_fullpath)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
