#!usr/bin/bash

#directory containing the google takeout .json file (change me!)
dir=02142019

#direct filepath to the  google takeout .json file (change me!)
RawJSON=$dir/location_history_02142019.json

#preferred output filename for the filtered .json file (change me!)
filteredJSON=$dir/filtered_locations_02142019.json

echo 'Filtering location history archive...'

`cat $RawJSON |jq "[.locations[] | {latitudeE7, longitudeE7, dirMs}]" > $filteredJSON`

echo 'Converting archive to csv...'

python3 csvParser.py $filteredJSON $dir

echo 'Making your movie, this may take a while...'

python3 coloranim.py $dir/FilteredLocationsFull.csv $dir/MyTravels_.mp4