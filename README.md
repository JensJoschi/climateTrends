# overview  
-work in progress- 

This program visualises temperature change over the last decades for a given location. It displays annual mean temperature at the site (based on weather data), as well as a linear trendline. The data uses (preprocessed) weather station data from the GHCN-daily dataset by NOAA. 
A linear regression is used to calculate the trend. 

This repo does not perform a valid, scientific analysis. it is meant for demonstration purposes only.

# Files
- station.py:  The climate station class represents one climate station. Takes data as input, and stores summary statistics after preprocessing (raw data is discarded)
- preprocessing.py: Processes raw data, filters stations with reliable data and stores the results in binary format (pickle)
- services.py: functions to load and find the closest climate station

# State:
[x] data preprocessing  
[x] Tests  
[x] algorithms to find and open nearest station  
[ ] UI  
[ ] pretty displaying of results  