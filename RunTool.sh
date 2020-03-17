#!usr/bin/bash

#directory containing the google takeout .json file (change me!)
dir=json-files
date=20191128

#location of the google takeout .json file (change me!)
RawJSON=$dir/Location-History_$date.json
echo $RawJSON

#name the output .json file (only change me if you have to!)
filteredJSON=$dir/filtered_locations_$date.json

# STEP 1: MAKE A CSV FILE
echo 'Filtering location history archive...'
`cat $RawJSON |jq "[.locations[] | {latitudeE7, longitudeE7, timestampMs, altitude, accuracy}]" > $filteredJSON`
echo $filteredJSON
echo 'Filtering complete'
python3 csvParser.py $filteredJSON $date