FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install pandas
RUN pip install SQLAlchemy

COPY ./app /app/app
