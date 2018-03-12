import os
import pandas

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

        self.address = location.address

        self.address_components = dict()

        # Load all the address components from the location parameter with a key that is the first value of
        # the types list and the value is the long_name of the component.
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
        if "street_number" in self.address_components.keys():
            return self.address_components["street_number"]

        else:
            return None

    def get_street_name(self):
        '''
        get_street_name returns the street name of this GoogleAddress.
        :return: <str | None> the street name or None if there is no street name known
        '''
        if "route" in self.address_components.keys():
            return self.address_components["route"]

        else:
            return None

    def get_city(self):
        '''
        get_city returns the city of this GoogleAddress.
        :return: <str | None> the city or None if there is no zip code known
        '''
        if "locality" in self.address_components.keys():
            return self.address_components["locality"]

        else:
            return None

    def get_zip_code(self):
        '''
        get_zip_code returns the zip code of this GoogleAddress.
        :return: <str | None> the zip code or None if there is no zip_code known
        '''
        if "postal_code" in self.address_components.keys():
            return self.address_components["postal_code"]

        else:
            return None

    def get_county(self):
        '''
        get_county returns the county of this GoogleAddress.
        :return: <str | None> the county or None if there is no county known
        '''
        if "administrative_area_level_2" in self.address_components.keys():
            return self.address_components["administrative_area_level_2"]

        else:
            return None

    def get_state(self):
        '''
        get_state returns the state of this GoogleAddress.
        :return: <str | None> the state or None if there is no state known
        '''
        if "administrative_area_level_1" in self.address_components.keys():
            return self.address_components["administrative_area_level_1"]

        else:
            return None

    def get_country(self):
        '''
        get_country returns the country of this GoogleAddress.
        :return: <str | None> the country or None if there is no country known
        '''
        if "country" in self.address_components.keys():
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
    LocationService connects to Google's geocoder.
    '''

    def __init__(self, google_api_key):
        self.geolocator = GoogleV3(google_api_key)

    def get_address(self, latitude, longitude):
        str_coordinates = "%f, %f" % (latitude, longitude)
        location = self.geolocator.reverse(str_coordinates, exactly_one=True)
        return GoogleAddress(location)


def read_airport_data(data_path, locator):
    data = pandas.read_csv(data_path)

    # Remove unnecessary columns.
    data = data.filter(["id", "ident", "type", "name", "latitude_deg", "longitude_deg", "elevation_ft",
                        "iso_country", "iso_region", "municipality"])

    # Keep only the entries that are in the continental US.
    data = data.loc[(data["iso_country"] == "US") & (~data["iso_region"].isin(["US-AK", "US-HI"]))]

    # Reduce the data size. (This is for testing only.)
    data = data.iloc[0:10]

    # Get the address of each airport.
    data["zip_code"] = data.apply(lambda x: locator.get_address(x['latitude_deg'], x['longitude_deg']).get_zip_code(),
                                 axis=1)

    return data


def read_sighting_data(data_path, locator):
    data = pandas.read_csv(data_path)

    return data


def read_meteorite_data(data_path, locator):
    data = pandas.read_csv(data_path)

    return data


def save_data(data):
    pass


load_dotenv("./.env")

google_api_key = os.getenv("GOOGLE_API_KEY")

locator = LocationService(google_api_key)

airport_data = read_airport_data("./RawData/airports.csv", locator)
print(airport_data)

#sighting_data = read_sighting_data("./RawData/complete.csv")

#meteorite_data = read_meteorite_data("./RawData/Meteorite_Landings.csv")

#save_data(airport_data)

#save_data(sighting_data)

#save_data(meteorite_data)
