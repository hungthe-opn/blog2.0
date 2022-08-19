# pull official base image
FROM python:3.8.10

# set environment varibles
ENV PYTHONUNBUFFERED 1
RUN mkdir /code/

# set work directory
WORKDIR /code/

# install dependencies
COPY requirements.txt /code/
RUN apt-get update
RUN apt-get install -y default-libmysqlclient-dev
RUN apt-get install -y gcc
RUN pip install --upgrade pip && pip install -r requirements.txt

# copy project
COPY . /code/

# NOTE:
#  + Disable auto migration
#  + Run migration manually, copy prod env file, exec in docker container and run cmd: python manage.py migrate

# Expose port 8000 and start Python server