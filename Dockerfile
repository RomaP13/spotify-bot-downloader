FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install ffmpeg for converting tracks
RUN apt-get update && apt-get install -y ffmpeg

# Install make utility
RUN apt-get install make

# Copy the Pipfile and Pipfile.lock to the container
COPY Pipfile Pipfile.lock /app/

# Install pipenv and dependencies
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# Copy the current directory contents into the container at /app
COPY . /app

# Create directories
RUN make setup
