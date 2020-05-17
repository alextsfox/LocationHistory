#Location History Mapping Tool

If you have location tracking turned on on your google account, this tool turns data into a nice looking animation. 

**Bash Dependencies:**

    jq   
  
**Python3 dependencies:**

    pandas
  
**R dependencies:**  

    tidyverse
    ggplot2

**To use:**
1. download your google location history data as a .json archive using takeout.google.com and place the unzipped directory in the working directory.
2. Change RunTool.sh to point towards the correct files. 
3. Run the script RunTool.sh:
4. Open R file, follow instructions.

**Credit**

Google Timeline Parser to filter the .json archive: https://github.com/javier/google_timeline_parser
