#!usr/bin/bash

timestamp=02142019
RawJSON=02142019/location_history_02142019.json
filteredJSON=02142019/filtered_locations_timestamped_02142019.json

#`cat $RawJSON |jq "[.locations[] | {latitudeE7, longitudeE7, timestampMs}]" > $filteredJSON`

python3 csvParser.py $filteredJSON $timestamp