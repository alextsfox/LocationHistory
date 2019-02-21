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
Resolution=15k

python3 colorImage.py $dir/FilteredLocations$Resolution.csv $dir/figs/MyTravels_$Resolution.png

echo 'Making your movie, this will take a long time...'

python3 coloranim_efficient.py $dir/FilteredLocations$Resolution.csv $dir/frames_$Resolution
python3 makeAnimateFromNPY.py $dir/frames_$Resolution.npy $dir/figs/MyTravels_$Resolution.mp4