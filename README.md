# ufo-sightings
A project for Databases class where ufo sightings are compared to known military base locations, 
airport locations and meteorite sightings.

## How To Clean The Data
1. Make sure that the following .csv files are in the RawData folder:
    * airports.csv - the airport location data (AirportData.csv when cleaned)
    * complete.csv - the ufo sighting data (UFOSightingData.csv when cleaned)
    * Meteorite_Landing.csv - the meteorite sighting datat (MeteoriteData.csv when cleaned)
    * MilitaryBases.geojson - the military base data (MilitaryBaseData.csv when cleaned)
1. Make sure that there is a .env file in this project with the following line:
    * `GOOGLE_API_KEY=<Your Google API Key>`
1. Run the data_prep.py file.
1. The cleaned data will appear in the CleanData folder.

## How To Put The Data In The Database
1. Make sure that Mariadb is installed on the computer.
1. Turn Mariadb on by using the command `$ mysql.server start`
1. Make sure that there is a .env file in this project with the following lines:
    * `DB_USER_NAME=<Your Mariadb User Name>`
    * `DB_PASSWORD=<Your Mariadb Password>`
1. Run the database_creation.py file.
1. A database called "ufo" should be created with the following tables:
    * AirportData - the table will all the airport locations
    * MeteoriteData - the table with all the meteorite data
    * MilitaryBaseData - the table with all the military base locations
    * UFOSightingData - the table with all the ufo sightings
