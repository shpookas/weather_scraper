#!/bin/bash

# List of cities for which we want temperature data
cities=("Zurich" "London" "Miami" "Tokyo" "Singapore")

# IPFS daemon address
REMOTE_IPFS_ADDRESS="/ip4/10.244.0.21/tcp/5001"

# Variable to hold all weather data
all_weather_data="["

# Function to scrape weather data for a city and append it to the all_weather_data variable
scrape_city_weather() {
    city="$1"
    temperature_data=$(curl -sS "https://wttr.in/$city?format=%t")
    current_datetime=$(date +"%Y-%m-%d %H:%M:%S")
    all_weather_data+="{\"city\": \"$city\", \"temperature\": \"$temperature_data\", \"datetime\": \"$current_datetime\"},"
}

# Iterate over each city and scrape its weather data
for city in "${cities[@]}"; do
    scrape_city_weather "$city"
done

# Remove the trailing comma from the last entry
all_weather_data="${all_weather_data%,}"

# Close the JSON array
all_weather_data+="]"

# Add all weather data to IPFS
ipfs_cid=$(echo "$all_weather_data" | ipfs --api "$REMOTE_IPFS_ADDRESS" add -Q)

echo "Added weather data for all cities to IPFS with CID: $ipfs_cid"
