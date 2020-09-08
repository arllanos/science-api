FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install pandas
RUN pip install SQLAlchemy
RUN pip install alembic

COPY ./app /app

WORKDIR /app