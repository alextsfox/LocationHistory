#!usr/bin/bash

#directory containing the google takeout .json file (change me!)
dir=Takeout/Location-History

#location of the google takeout .json file (change me!)
RawJSON=$dir/Location-History.json

#name the output .json file (only change me if you have to!)
filteredJSON=$dir/filtered_locations_.json

mkdir -p $dir/figs

# STEP 1: MAKE A CSV FILE
echo 'Filtering location history archive...'
`cat $RawJSON |jq "[.locations[] | {latitudeE7, longitudeE7, timestampMs}]" > $filteredJSON`
python3 csvParser.py $filteredJSON

# STEP 2: MAKE A PNG FILE

# set the borders of your image, decimal degrees (change me!)
N=85
S=-85
W=-179.9
E=179.9

#Usage: colorImage.py <.csv file path> <.png output filename>
python3 colorImage.py $dir/FilteredLocations_Full.csv $dir/figs/My_Travels_Full.png -t $N $W $S $E

# STEP3: MAKE A MOVIE
echo 'Making your movie, this will take a long time...'

#usage: coloranim_efficient.py <.csv file path>
python3 coloranim_efficient.py $dir/FilteredLocations_Full.csv -t $N $W $S $E

# usage: makeAnimateFromNPY.py <.mp4 output filename> <optional argument -v turns on analytics>
python3 makeAnimateFromNPY.py $dir/figs/My_Travels_Full.mp4 -t $N $W $S $E -v