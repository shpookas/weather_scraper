# Use an official Python runtime as a parent image
FROM python:alpine3.19

# Set the working directory in the container
WORKDIR /usr/src/app

# Install build dependencies
RUN apk --no-cache add build-base librdkafka-dev

# Copy the local code into the container at the working directory
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the application
CMD ["python", "./scraper.py"]
