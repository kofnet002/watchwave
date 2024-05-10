FROM python:3

ENV PYTHONUNBUFFERED 1
RUN mkdir /watchwave_api
WORKDIR /watchwave_api
COPY . /watchwave_api/
RUN pip install -r requirements.txt