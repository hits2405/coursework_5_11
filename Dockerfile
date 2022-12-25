FROM python:3.8.5

WORKDIR /code
COPY data/requirements.txt .
RUN pip install -r requirements.txt
COPY . .