#!usr/bin/bash

timestamp=02142019
RawJSON=$timestamp/location_history_$timestamp.json
filteredJSON=$timestamp/filtered_locations_timestamped_$timestamp.json

`cat $RawJSON |jq "[.locations[] | {latitudeE7, longitudeE7, timestampMs}]" > $filteredJSON`

python3 csvParser.py $filteredJSON $timestamp