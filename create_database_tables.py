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


def create_cross_table(table_a, table_b, max_distance):
    result = pandas.DataFrame(columns=["a_id", "b_id", "distance_miles"])

    for i, a_row in table_a.iterrows():

        a_id = a_row["id"]
        a_coordinates = (a_row["latitude_deg"], a_row["longitude_deg"])

        for j, b_row in table_b.iterrows():
            b_id = b_row["id"]
            b_coordinates = (b_row["latitude_deg"], b_row["longitude_deg"])

            distance = great_circle(a_coordinates, b_coordinates).miles

            if distance <= max_distance:
                result.loc[len(result)] = [a_id, b_id, distance]

        print("Number %s of %s" % (str(i), str(len(table_a))))

    return result


def create_military_ufo_sightings_mapping_table(military_table, sightings_table, max_distance=10):
    result = create_cross_table(military_table, sightings_table, max_distance)
    result = result.rename(columns={"a_id": "military_id", "b_id": "sightings_id"})
    return result


def create_airport_ufo_sightings_mapping_table(airport_table, sightings_table, max_distance=10):
    result = create_cross_table(airport_table, sightings_table, max_distance)
    result = result.rename(columns={"a_id": "airport_id", "b_id": "sightings_id"})
    return result


def get_addresses(table):
    result = pandas.DataFrame(columns=["latitude_deg", "longitude_deg", "city", "zip_code",
                                       "county", "state", "country"])

    for i, row in table.iterrows():
        result.loc[len(result)] = [row["latitude_deg"], row["longitude_deg"], row["city"],
                                   row["zip_code"], row["county"], row["state"], row["country"]]

    return result


def create_address_table(military_data, airport_data, sightings_data):

    military_addresses = get_addresses(military_data)
    airport_addresses = get_addresses(airport_data)
    sightings_data = get_addresses(sightings_data)

    addresses = military_addresses.append(airport_addresses)
    addresses = addresses.append(sightings_data)

    return addresses


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

    military_X_sightings_table = create_military_ufo_sightings_mapping_table(military_table, sighting_table,
                                                                             max_distance=10)
    military_X_sightings_table.to_csv("./DatabaseTables/MilitaryXSightingsTable", index=False)

    airport_X_sightings_table = create_airport_ufo_sightings_mapping_table(airport_table, sighting_table,
                                                                           max_distance=10)
    airport_X_sightings_table.to_csv("./DatabaseTables/AirportXSightingsTable", index=False)

    address_table = create_address_table(military_data, airport_data, sighting_data)
    address_table.to_csv("./DatabaseTables/AddressTable", index=False)
