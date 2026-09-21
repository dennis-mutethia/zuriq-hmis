# Use python base image
FROM python:3.14-slim

# Update packages, install uuidgen, and clean up
RUN apt-get update \
    && apt-get install -y git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
#update pip & install dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt
   
COPY . .

# Set the timezone to Africa/Nairobi
RUN ln -sf /usr/share/zoneinfo/Africa/Nairobi /etc/localtime

EXPOSE 8000
