#Location History Mapping Tool

If you have location tracking turned on on your google account, this tool turns data into a nice looking animation. 

**Bash Dependencies:**

    jq   
  
**Python3 dependencies:**

    pandas
  
**R dependencies:**  

    tidyverse
    ggplot2
    maps
    lubridate
    anytime

**To use:**
1. download your google location history data as a .json archive using takeout.google.com and place the `json-files` directory.
2. Rename the downloaded .json file to `Location-History_yyyymmdd.json`, where yyyymmdd is today's date.
2. Open RunTool.sh, change the necessary lines. 
3. Run the script RunTool.sh
4. Open the R file and follow the instructions there.

**Credit**

Google Timeline Parser to filter the .json archive: https://github.com/javier/google_timeline_parser
