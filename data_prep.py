import os
import pandas

from dotenv import load_dotenv
from geopy.geocoders import GoogleV3


class GoogleAddress:

    def __init__(self, location):
        self.address = location.address

        self.address_components = dict()

        for value in location.raw["address_components"]:
            self.address_components[value["types"][0]] = value["long_name"]

    def get_address(self):
        return self.address

    def get_house_number(self):
        if "street_number" in self.address_components.keys():
            return self.address_components["street_number"]

        else:
            return None

    def get_street_name(self):
        if "route" in self.address_components.keys():
            return self.address_components["route"]

        else:
            return None

    def get_city(self):
        if "locality" in self.address_components.keys():
            return self.address_components["locality"]

        else:
            return None

    def get_zip_code(self):
        if "postal_code" in self.address_components.keys():
            return self.address_components["postal_code"]

        else:
            return None

    def get_county(self):
        if "administrative_area_level_2" in self.address_components.keys():
            return self.address_components["administrative_area_level_2"]

        else:
            return None

    def get_state(self):
        if "administrative_area_level_1" in self.address_components.keys():
            return self.address_components["administrative_area_level_1"]

        else:
            return None

    def get_country(self):
        if "country" in self.address_components.keys():
            return self.address_components["country"]

        else:
            return None

    def __str__(self):
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


def read_sighting_data(data_path):
    data = pandas.read_csv(data_path)

    return data


def read_meteorite_data(data_path):
    data = pandas.read_csv(data_path)

    return data


def save_data(data):
    pass


load_dotenv("./.env")

google_api_key = os.getenv("GOOGLE_API_KEY")

locator = LocationService(google_api_key)

airport_data = read_airport_data("./RawData/airports.csv", locator)
print(airport_data)

#ighting_data = read_sighting_data("./RawData/complete.csv")

#meteorite_data = read_meteorite_data("./RawData/Meteorite_Landings.csv")

#save_data(airport_data)

#save_data(sighting_data)

#save_data(meteorite_data)
