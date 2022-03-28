FROM python:3.10.4-slim-bullseye

WORKDIR /opt/orange_users

COPY ./requirements.txt /opt/orange_users/requirements.txt

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r /opt/orange_users/requirements.txt

COPY . /opt/orange_users

ENV PYTHONPATH=/opt/orange_users
