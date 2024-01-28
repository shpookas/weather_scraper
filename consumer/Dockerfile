# Use an official Python runtime as a parent image
FROM python:3

# Set the working directory in the container
WORKDIR /usr/src/app

# Install the PostgreSQL development package for Alpine
# RUN apk --no-cache add postgresql-dev build-base librdkafka-dev
#RUN apt postgresql-dev build-base librdkafka-dev

# Install PostgreSQL development headers and build tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql-server-dev-all \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install librdkafka development headers
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    librdkafka-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the local code into the container at the working directory
COPY . .

# Pip install psycopg2 since its causing a lot of problems
RUN pip install psycopg2-binary
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the application
CMD ["python", "./kafka_consumer.py"]
