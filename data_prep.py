import os
import pandas

from dotenv import load_dotenv
from geopy.geocoders import GoogleV3


class LocationService:
    '''
    LocationService connects to Google's geocoder.
    '''

    def __init__(self, google_api_key):
        self.geolocator = GoogleV3(api_key=google_api_key)

    def get_address(self, latitude, longitude):
        str_coordinates = "%f, %f" % (latitude, longitude)
        address = self.geolocator.reverse(str_coordinates, exactly_one=True)
        return address


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
    data["address"] = data.apply(lambda x: locator.get_address(x['latitude_deg'], x['longitude_deg']),
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

#ighting_data = read_sighting_data("./RawData/complete.csv")

#meteorite_data = read_meteorite_data("./RawData/Meteorite_Landings.csv")

#save_data(airport_data)

#save_data(sighting_data)

#save_data(meteorite_data)
