#!/bin/bash

# List of cities for which we want temperature data
cities=("Zurich" "London" "Miami" "Tokyo" "Singapore")

# Variable to hold all weather data
all_weather_data="["

# IPFS daemon address
REMOTE_IPFS_ADDRESS="/ip4/10.244.0.11/tcp/5001"

# Function to scrape weather data for a city and append it to the all_weather_data variable
scrape_city_weather() {
    city="$1"
    temperature_data=$(curl -sS "https://wttr.in/$city?format=%t")
    current_datetime=$(date +"%Y-%m-%d %H:%M:%S")
    all_weather_data+="\n    {\"city\": \"$city\", \"temperature\": \"$temperature_data\", \"datetime\": \"$current_datetime\"},"
}

# Iterate over each city and scrape its weather data
for city in "${cities[@]}"; do
    scrape_city_weather "$city"
done
gi
# Remove the trailing comma from the last entry and close the JSON array
all_weather_data="${all_weather_data%,}\n]"

# Create a simple HTTP server using netcat to serve the weather data
while true; do
    ipfs_cid=$(echo "$all_weather_data" | ipfs --api "$REMOTE_IPFS_ADDRESS" add -Q)
    ipfs_message="Added weather data for all cities to IPFS with CID: $ipfs_cid"
    (
    echo -e "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: $(echo -n "$all_weather_data\n$ipfs_message" | wc -c)\r\n\r\n$all_weather_data\n$ipfs_message"
    ) | nc -l -p 8080 -q 1
done
