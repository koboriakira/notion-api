FROM python:3.11-slim

WORKDIR /workspace

# install git
RUN apt update && \
  apt install -y git
RUN apt clean

# Python dependencies
COPY ./requirements.txt .
RUN pip install -U pip \
    && pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install uvicorn
