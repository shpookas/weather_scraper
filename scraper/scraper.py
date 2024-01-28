import json
import requests
from confluent_kafka import Producer
import schedule
import time


# Configure Kafka producer
conf = {
    'bootstrap.servers': 'kafka:9092',  # Replace with Kafka broker in Kubernetes (kafka service)
}

# Create a Kafka producer instance
producer = Producer(conf)
print("Connected to kafka")

# Kafka topic to produce messages
topic = 'temperature'  # Replace with your desired Kafka topic

# List of cities for which we want temperature data
cities = ['Zurich', 'London', 'Miami', 'Tokyo', 'Singapore']

def fetch_and_produce():
    for city in cities:
        try:
            # Fetch temperature data from wttr.in
            wttr_url = f'https://wttr.in/{city}?format=%t'
            temperature_data = requests.get(wttr_url).text.strip()

            # Create a JSON message with city and temperature data
            message = json.dumps({'city': city, 'temperature': temperature_data})

            # Produce the message to the Kafka topic
            producer.produce(topic, key=city.encode('utf-8'), value=message.encode('utf-8'))

            print(f"Produced message for {city}: {temperature_data}")

        except Exception as e:
            print(f"Error fetching temperature data for {city}: {e}")

# Schedule the job to run every hour
schedule.every().minute.do(fetch_and_produce)

while True:
    # Run pending scheduled jobs
    schedule.run_pending()
    time.sleep(1)  # Sleep for 1 second to avoid high CPU usage
