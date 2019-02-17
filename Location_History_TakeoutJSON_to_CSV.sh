#!usr/bin/bash

timestamp=02142019
RawJSON=$timestamp/location_history_$timestamp.json
filteredJSON=$timestamp/filtered_locations_timestamped_$timestamp.json

echo 'Filtering location history archive...'

`cat $RawJSON |jq "[.locations[] | {latitudeE7, longitudeE7, timestampMs}]" > $filteredJSON`

echo 'Converting archive to csv...'

python3 csvParser.py $filteredJSON $timestamp

echo 'Making your movie, this may take a while...'

python3 coloranim.py $timestamp/FilteredLocationsFull_$timestamp.csv $timestamp/MyTravels_$timestamp.mp4