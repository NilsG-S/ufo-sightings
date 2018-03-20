import os
import pandas
import pickle
import atexit

from dotenv import load_dotenv
from geopy.geocoders import GoogleV3


class GoogleAddress:
    '''
    GoogleAddress is a parsed address taken from the location produced after calling reverse on the
    GoogleV3 geopy.geocoders.
    '''

    def __init__(self, location):
        '''
        :param location: <geopy.Location> this is the object that is returned from the geopy.geocoders.GoogleV3
            when the revese method is called.

        Class Variables:
        self.address: <str> a string that represents the address
        self.address_components: <dict <str, str>> a dictionary that keeps all the components of the address
        '''

        if location is None:
            self.address = ""
            self.address_components = dict()

        else:
            self.address = location.address

            self.address_components = dict()

            # Load all the address components from the location parameter with a key that is the first
            # value of the types list and the value is the long_name of the component.
            for value in location.raw["address_components"]:
                self.address_components[value["types"][0]] = value["long_name"]

    def get_address(self):
        '''
        get_address returns the address of this GoogleAddress.
        :return: <str> the address as a string
        '''

        return self.address

    def get_house_number(self):
        '''
        get_house_number returns the house number of this GoogleAddress.
        :return: <str | None> the house number or None if there is no house number known
        '''

        if "street_number" in self.address_components:
            return self.address_components["street_number"]

        else:
            return None

    def get_street_name(self):
        '''
        get_street_name returns the street name of this GoogleAddress.
        :return: <str | None> the street name or None if there is no street name known
        '''

        if "route" in self.address_components:
            return self.address_components["route"]

        else:
            return None

    def get_city(self):
        '''
        get_city returns the city of this GoogleAddress.
        :return: <str | None> the city or None if there is no zip code known
        '''

        if "locality" in self.address_components:
            return self.address_components["locality"]

        else:
            return None

    def get_zip_code(self):
        '''
        get_zip_code returns the zip code of this GoogleAddress.
        :return: <str | None> the zip code or None if there is no zip_code known
        '''

        if "postal_code" in self.address_components:
            return self.address_components["postal_code"]

        else:
            return None

    def get_county(self):
        '''
        get_county returns the county of this GoogleAddress.
        :return: <str | None> the county or None if there is no county known
        '''

        if "administrative_area_level_2" in self.address_components:
            return self.address_components["administrative_area_level_2"]

        else:
            return None

    def get_state(self):
        '''
        get_state returns the state of this GoogleAddress.
        :return: <str | None> the state or None if there is no state known
        '''

        if "administrative_area_level_1" in self.address_components:
            return self.address_components["administrative_area_level_1"]

        else:
            return None

    def get_country(self):
        '''
        get_country returns the country of this GoogleAddress.
        :return: <str | None> the country or None if there is no country known
        '''

        if "country" in self.address_components:
            return self.address_components["country"]

        else:
            return None

    def __str__(self):
        '''
        __str__ returns the full address as a string
        :return: <str> the full address
        '''

        return self.address


class LocationService:
    '''
    LocationService gives addresses based on coordinates.
    '''

    def __init__(self, google_api_key, file_path="./addresses.dict"):
        '''
        :param google_api_key: <str> a google api key to use
        :param file_path: <str> the file path to where to load the saved addresses to
            and where to save the addresses to
            Default Value: "./addresses.dict"
        Class Variables:
        self.geolocator: <geopy.gecoders.GoogleV3> the geocoder that connects to google to
            get address information
        self.file_path: <str> the file path to where to load the saved addresses to
            and where to save the addresses to
        self.addresses: <dict <(float latitude, float longitude): GoogleAddress address> a dictionary
            that maps a latitude, longitude coordinate pair to the GoogleAddress at that position.
        '''

        self.geolocator = GoogleV3(google_api_key)

        self.file_path = file_path

        self.addresses = self.load_addresses(self.file_path)

        # Register the function self.save_addresses to run when object is deleted.
        atexit.register(self.save_addresses)

    def load_addresses(self, file_path):
        '''
        load_addresses loads the pickled addresses dictionary data.
        :param file_path: <str> the file path to try to load the addresses dictionary from
        :return: <dict <(float latitude, float longitude): GoogleAddress address> the addresses dictionary
            loaded from the file at file_path or an empty dictionary if there is no file at file_path
        '''

        addresses = dict()

        if os.path.exists(file_path):
            file = open(file_path, "rb")
            addresses = pickle.load(file)
            file.close()

        return addresses

    def save_addresses(self):
        '''
        save_addresses pickles and saves self.addresses to the file path self.file_path.
        :return: None
        '''

        file = open(self.file_path, "wb")
        pickle.dump(self.addresses, file)
        file.close()

    def get_address(self, latitude, longitude):
        '''
        get_address gets the GoogleAddress that corresponds to the latitude and longitude
        given.
        :param latitude: <float> valid latitude
        :param longitude: <float> valid longitude
        :return: <GoogleAddress> the address that corresponds to the latitude and longitude supplied
        '''

        # If the latitude, longitude pair has already been found, return that value.
        if (latitude, longitude) in self.addresses:
            return self.addresses[(latitude, longitude)]

        else:
            # Turn the coordinate pair into a string to pass to Google.
            str_coordinates = "%f, %f" % (latitude, longitude)

            # Have the GoogleV3 geolocator get the location from Google.
            location = self.geolocator.reverse(str_coordinates, exactly_one=True)

            # Change the location into a GoogleAddress
            address = GoogleAddress(location)

            # Store the newly found GoogleAddress
            self.addresses[(latitude, longitude)] = address

            return address


def read_airport_data(data_path, locator):
    '''
    read_airport_data reads in the airport data located at data_path and cleans the data.
    :param data_path: <str> the data_path where the airport data is located
    :param locator: <LocationService> the LocationService to use to get the addresses for the data
    :return: <pandas.DataFrame> the cleaned airport data
    '''

    data = pandas.read_csv(data_path)

    # Remove unnecessary columns.
    data = data.filter(["id", "ident", "type", "name", "latitude_deg", "longitude_deg", "elevation_ft",
                        "iso_country", "iso_region", "municipality"])

    # Rename some of the columns to better names.
    data = data.rename(columns={"ident": "airport_code", "iso_country": "country",
                                "iso_region": "state", "municipality": "city"})

    # Turn the values in the states column into just state codes.
    data["state"] = data.apply(lambda x: x["state"].split('-', 1)[1], axis=1)

    # Excluding airports that are closed, heliports or small.
    excluded_types = ["closed", "heliport", "small_airport"]

    # Keep only the entries that are in the continental US and are not of an excluded type.
    data = data.loc[(data["country"] == "US") & (~data["state"].isin(["US-AK", "US-HI"])) &
                    (~data["type"].isin(excluded_types))]

    # Get the zip code of each airport.
    data["zip_code"] = data.apply(lambda x: locator.get_address(x['latitude_deg'], x['longitude_deg']).get_zip_code(),
                                 axis=1)

    return data


def read_sighting_data(data_path, locator):
    '''
    read_sighting_data reads in the ufo sighting data located at data_path and cleans the data.
    :param data_path: <str> the data_path where the ufo sighting data is located
    :param locator: <LocationService> the LocationService to use to get the addresses for the data
    :return: <pandas.DataFrame> the cleaned ufo sighting data
    '''

    data = pandas.read_csv(data_path, converters={"latitude": str, "longitude": str})

    # Remove unnecessary columns.
    data = data.filter(["datetime", "city", "state", "country", "shape", "duration (seconds)", "latitude",
                        "longitude"])

    # Rename some of the columns to better names.
    data = data.rename(columns={"datetime": "date_time", "duration (seconds)": "duration_seconds",
                                "latitude": "latitude_deg", "longitude": "longitude_deg"})

    # Keep only the entries that are in the continental US.
    data = data.loc[(data["country"] == "us") & (~data["state"].isin(["as", "hi"]))]

    # Keep only the entries where date_time follows the format "mm/dd/yy hh:mm".
    data = data.loc[(data["date_time"].str.match("\\d+/\\d+/\\d+ \\d+:\\d+"))]

    # Keep only valid floats for latitudes and convert them to floats.
    data = data.loc[(data["latitude_deg"].str.match("-?\\d+(\\.\\d+)?"))]
    data["latitude_deg"] = data.apply(lambda x: float(x["latitude_deg"]), axis=1)

    # Keep only valid floats for longitudes and convert them to floats.
    data = data.loc[(data["longitude_deg"].str.match("-?\\d+(\\.\\d+)?"))]
    data["longitude_deg"] = data.apply(lambda x: float(x["longitude_deg"]), axis=1)

    # Remove all entries where the longitude and latitude are zero.
    data = data.loc[(data["latitude_deg"] != 0) & (data["longitude_deg"] != 0)]

    # Create a date column taken from the date_time column.
    data["date"] = data.apply(lambda x: x["date_time"].split(' ', 1)[0], axis=1)

    # Create a time column taken from the date_time column.
    data["time"] = data.apply(lambda x: x["date_time"].split(' ', 1)[1], axis=1)

    # Get the two digit year for each date.
    data["year"] = data.apply(lambda x: int(x["date"].split('/', 2)[2]), axis=1)

    # Filter out all the years that are not between 2010 and 2018.
    data = data[data["year"].between(10, 18, inclusive=True)]

    # Turn the values in the states column into uppercase.
    data["state"] = data.apply(lambda x: x["state"].upper(), axis=1)

    # Turn the values in the country column into uppercase.
    data["country"] = data.apply(lambda x: x["country"].upper(), axis=1)

    # Turn the values in the city column into title case.
    data["city"] = data.apply(lambda x: x["city"].title(), axis=1)

    # Get the address of each sighting.
    data["zip_code"] = data.apply(lambda x: locator.get_address(x['latitude_deg'], x['longitude_deg']).get_zip_code(),
                                  axis=1)

    data = data.filter(["date", "time", "city", "state", "country", "zip_code", "shape", "duration_seconds",
                        "latitude_deg", "longitude_deg"])

    return data


def read_meteorite_data(data_path, locator):
    '''
    read_meteorite_data reads in the meteorite data located at data_path and cleans the data.
    :param data_path: <str> the data_path where the meteorite data is located
    :param locator: <LocationService> the LocationService to use to get the addresses for the data
    :return: <pandas.DataFrame> the cleaned meteorite data
    '''

    data = pandas.read_csv(data_path)

    # Remove unnecessary columns.
    data = data.filter(["name", "id", "mass (g)", "fall", "year", "reclat", "reclong"])

    # Rename some of the columns to better names.
    data = data.rename(columns={"mass (g)": "mass_grams", "year": "date_time",
                                "reclat": "latitude_deg", "reclong": "longitude_deg"})

    data = data.loc[(~data["date_time"].isnull()) & (~data["mass_grams"].isnull()) &
                    (~data["latitude_deg"].isnull()) & (~data["longitude_deg"].isnull()) &
                    (data["fall"] == "Fell")]

    # Keep only the entries where date_time follows the format "mm/dd/yy hh:mm:ss AM or PM".
    data = data.loc[(data["date_time"].str.match("\\d+/\\d+/\\d+ \\d+:\\d+:\\d+ (AM|PM)"))]

    # Create a date column taken from the date_time column.
    data["date"] = data.apply(lambda x: x["date_time"].split(' ', 1)[0], axis=1)

    # Create a time column taken from the date_time column.
    data["time"] = data.apply(lambda x: x["date_time"].split(' ', 1)[1], axis=1)

    # Get the zip code of each sighting.
    data["zip_code"] = data.apply(lambda x: locator.get_address(x['latitude_deg'], x['longitude_deg']).get_zip_code(),
                                  axis=1)

    # Get the country of each sighting.
    data["country"] = data.apply(lambda x: locator.get_address(x['latitude_deg'], x['longitude_deg']).get_country(),
                                 axis=1)

    # Keep only the entries where the country is the United States.
    data = data.loc[data['country'] == "United States"]

    # Get the two digit year for each date.
    data["year"] = data.apply(lambda x: int(x["date"].split('/', 2)[2]), axis=1)

    # Filter out all the years that are not between 2010 and 2018.
    data = data[data["year"].between(2010, 2018, inclusive=True)]

    data = data.filter(["name", "id", "mass_grams", "date", "time", "country", "zip_code"])

    return data


# Load the environment file for environment variable.
load_dotenv("./.env")

# Load the Google API Key from the environment file.
google_api_key = os.getenv("GOOGLE_API_KEY")

# Create a LocationService object with the Google API Key.
locator = LocationService(google_api_key)

# Clean and save the airport data.
airport_data = read_airport_data("./RawData/airports.csv", locator)
airport_data.to_csv("./CleanData/AirportData.csv", index=False)

# Clean and save the ufo sighting data.
sighting_data = read_sighting_data("./RawData/complete.csv", locator)
sighting_data.to_csv("./CleanData/UFOSightingData.csv", index=False)

# Clean and save the meteorite data.
meteorite_data = read_meteorite_data("./RawData/Meteorite_Landings.csv", locator)
meteorite_data.to_csv("./CleanData/MeteoriteData.csv", index=False)
