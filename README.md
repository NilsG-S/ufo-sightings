# ufo-sightings
A project for Databases class where ufo sightings are compared to known military base locations, 
airport locations and meteorite sightings.

## How To Clean The Data
1. Make sure that the following .csv files are in the RawData folder:
    * airports.csv - the airport location data (AirportData.csv when cleaned)
    * complete.csv - the ufo sighting data (UFOSightingData.csv when cleaned)
    * MilitaryBases.geojson - the military base data (MilitaryBaseData.csv when cleaned)
1. Make sure that there is a .env file in this project with the following line:
    * `GOOGLE_API_KEY=<Your Google API Key>`
1. Run the clean_data.py file.
1. The cleaned data will appear in the CleanData folder.

## How To Create The Database Tables
1. Make sure that you have cleaned the data. (Process listed above.)
1. Make sure the following .csv files are in the CleanData folder:
    * AirportData.csv - the airport location data (AirportTable.csv, AirportXSightingsTable.csv and AddressTable.csv when tables created)
    * MilitaryBaseData.csv - the military base data (MilitaryTable.csv, MilitaryXSightingsTable.csv and AddressTable.csv when tables created)
    * UFOSightingData.csv - the ufo sighting data (UFOSightingsTable.csv, AirportXSightingsTable.csv, MilitaryXSightings and AddressTable.csv when tables created)
1. Run the create_database_tables.py file. (This may take quite a wile to complete.)
1. The created tables will appear in the DatabaseTables folder.

## How To Put The Data In The Database
1. Make sure that Mariadb is installed on the computer.
1. Turn Mariadb on by using the command `$ mysql.server start`.
1. Make sure that there is a .env file in this project with the following lines:
    * `DB_USER_NAME=<Your Mariadb User Name>`
    * `DB_PASSWORD=<Your Mariadb Password>`
1. Make sure the following .csv files are in the DatabaseTables folder:
    * AddressTable.csv - the address of all the airports, military bases and ufo sightings (Addresses when inserted)
    * AirportTable.csv - the airport location data (Airports when inserted)
    * AirportXSightingsTable.csv - the airports mapped to ufo sightings (AirportsXSightings when inserted)
    * MilitaryBaseTable.csv - the military location data (MilitaryBases when inserted)
    * MilitaryXSightings.csv - the military bases mapped to the ufo sightings (MilitaryBasesXSightings when inserted)
    * UFOSightingTable.csv - the ufo sightings location data (UFOSightings when inserted)
1. Run the database_creation.py file. 
    * <span style="color:red"><strong>Warning:</strong> This will not run on Windows unless the file 
    paths in the code are changed for Windows.</span>
1. A database called "ufo" should be created with the following tables:
    * Addresses - the addresses of the airports, military bases and ufo sightings
    * Airports - the table will all the airport locations
    * AirportsXSightings - the airports mapped to ufo sightings
    * MilitaryBases - the table with all the military base locations
    * MilitaryBasesXSightings - the military bases mapped to the ufo sightings
    * UFOSightings - the table with all the ufo sightings
