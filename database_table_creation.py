from geopy.distance import great_circle
import pandas


def create_military_table(military_data):
    return military_data.filter(["id", "name", "type", "latitude_deg", "longitude_deg"])


def create_airport_table(airport_data):
    return airport_data.filter(["id", "airport_code", "name", "type", "latitude_deg", "longitude_deg",
                                "elevation_ft"])


def create_ufo_sightings_table(sightings_data):
    return sightings_data.filter(["id", "date", "time", "shape", "duration_seconds", "latitude_deg",
                                  "longitude_deg"])


def create_military_ufo_sightings_mapping_table(military_table, sightings_table, max_distance=10):

    result = pandas.DataFrame(columns=["military_id", "sighting_id", "distance"])

    for i, sighting_row in sightings_table.iterrows():

        sighting_id = sighting_row["id"]
        sighting_coordinates = (sighting_row["latitude_deg"], sighting_row["longitude_deg"])

        for j, military_row in military_table.iterrows():
            military_id = military_row["id"]
            military_coordinates = (military_row["latitude_deg"], military_row["longitude_deg"])

            distance = great_circle(sighting_coordinates, military_coordinates).miles

            if distance <= max_distance:
                result.loc[len(result)] = [military_id, sighting_id, distance]



def create_airport_ufo_sightings_mapping_table(airport_data, sightings_data):
    pass


def create_address_table(military_data, airport_data, sightings_data):
    pass


if __name__ == "__main__":

    military_data = pandas.read_csv("./CleanData/MilitaryBaseData.csv")
    military_table = create_military_table(military_data)
    military_table.to_csv("./DatabaseTables/MilitaryBaseTable", index=False)

    airport_data = pandas.read_csv("./CleanData/AirportData.csv")
    airport_table = create_airport_table(airport_data)
    airport_table.to_csv("./DatabaseTables/AirportTable", index=False)

    sighting_data = pandas.read_csv("./CleanData/UFOSightingData.csv")
    sighting_table = create_ufo_sightings_table(sighting_data)
    sighting_table.to_csv("./DatabaseTables/UFOSightingTable", index=False)
