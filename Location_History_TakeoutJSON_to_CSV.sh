#!usr/bin/bash

#directory containing the google takeout .json file (change me!)
dir=LocDir02142019

#location of the google takeout .json file (change me!)
RawJSON=LocDir02142019/location_history_02142019.json


filteredJSON=$dir/filtered_locations_.json

echo 'Filtering location history archive...'

`cat $RawJSON |jq "[.locations[] | {latitudeE7, longitudeE7, timestampMs}]" > $filteredJSON`

echo 'Converting archive to csv...'

python3 csvParser.py $filteredJSON $dir

#select the resoltuion (choose between Ultra Low Res: '05k', Low Res: '15k', and Full Res: 'Full')
Resolution=Full

python3 coloranim.py $dir/FilteredLocations$Resolution.csv $dir/MyTravels_$Resolution.png

echo 'Making your movie, this will take a long time...'

python3 coloranim.py $dir/FilteredLocations$Resolution.csv $dir/MyTravels_$Resolution.mp4