#!usr/bin/bash

#directory containing the google takeout .json file (change me!)
dir=json-files

#date you downloaded the data, in yyyymmdd format (change me!)
date=20201229

#location of the google takeout .json file within the json-files directory
RawJSON=$dir/Location-History_$date.json
echo $RawJSON

#name the output .json file (only change me if you have to!)
filteredJSON=$dir/filtered_locations_$date.json

echo 'Filtering location history archive...'

# I don't really know what this line does
`cat $RawJSON |jq "[.locations[] | {latitudeE7, longitudeE7, timestampMs, altitude, accuracy}]" > $filteredJSON`

echo $filteredJSON
echo 'Filtering complete'

# Convert to CSV
python3 csvParser.py $filteredJSON $date