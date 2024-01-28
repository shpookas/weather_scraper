from confluent_kafka import Consumer, KafkaError
import psycopg2
import json
import time

# Configure Kafka consumer
conf = {
    'bootstrap.servers': 'kafka:9092',  # Replace with your Kafka broker(s)
    'group.id': '1',  # Consumer group ID
    'auto.offset.reset': 'earliest'  # Start reading from the beginning of the topic
}

# Create a Kafka consumer instance
consumer = Consumer(conf)
print ("Consumer created")

# Configure PostgreSQL connection
postgres_conf = {
    'host': 'postgres',     # Postgres service in k8s
    'port': '5432',
    'database': 'temperature_database',   # Replace with your PostgreSQL database
    'user': 'temperature_user',     # Replace with your PostgreSQL user
    'password': 'temperature_password'  # Replace witlh your PostgreSQL password
}

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(**postgres_conf)
    cursor = conn.cursor()
    print ("Connected to Postgres")
    # Create a table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS temperature_data (
            id SERIAL PRIMARY KEY,
            city VARCHAR(50),
            temperature VARCHAR(10),
            timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()


except Exception as e:
    print(f"Error connecting to PostgreSQL: {e}")
    exit()

# Subscribe to the Kafka topic
consumer.subscribe(['temperature'])  # Replace with your Kafka topic

try:
    while True:
        # Poll for messages
        
        msg = consumer.poll(5.0)  # check every 5 seconds for new messages

        if msg is None:
            print ("No new messages")
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event
                print(f"Reached end of partition {msg.partition()}")
            else:
                print(f"Error: {msg.error()}")
        else:
            # Process the received message
            try:
                #if msg.value():
                data = json.loads(msg.value().decode('utf-8'))
                # Insert data into PostgreSQL
                cursor.execute('''
                    INSERT INTO temperature_data (city, temperature)
                    VALUES (%s, %s)
                ''', (data['city'], data['temperature']))

                conn.commit()

                print(f"Inserted data for {data['city']} into PostgreSQL")
                #else:
                   # print("Received empty message value")

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")

except KeyboardInterrupt:
    pass
finally:
    # Close connections
    cursor.close()
    conn.close()

    # Close down consumer to commit final offsets.
    consumer.close()
