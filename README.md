## Covid-19 data analysis

Data collected from [nytimes](https://github.com/nytimes/covid-19-data/tree/bf69d9d204e064caf31b53091b341053e97e8b09) repo is analyzed to generate models for deaths due to Covid-19. Updated everyday.

### Filters
The ratio of mortality is calculated by shifting recorded mortality by n days and dividing each mortality value 
* Shift - Shifting of days for ratio calculation
* Trigger - Ratio of death when the mortality value is analyzed
* Days - Data of recent days when the slope for prediction is calculated 

### Requirements
1. Tested in python 3.6
2. ```pip install -r requirements.txt```


### Snapshot
![Mortality Projection Plot](snapshot/snapshot_mortalityProjection.PNG?raw=true "Mortality Projection Plot")
![Mortality Projection Maps](snapshot/snapshot_mortalityProjectionMaps.PNG?raw=true "Mortality Projection Maps")