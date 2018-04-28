from geopy.distance import great_circle
import pandas


def create_military_table(military_data):
    '''
    create_military_table creates the military table that should be placed into the database.
    :param military_data: <pandas.DataFrame> the cleaned military base data
    :return: <pandas.DataFrame> the military table that should be placed into the database
    '''

    return military_data.filter(["id", "name", "type", "latitude_deg", "longitude_deg"])


def create_airport_table(airport_data):
    '''
    create_airport_table creates the airport table that should be placed into the database.
    :param airport_data: <pandas.DataFrame> the cleaned airport base data
    :return: <pandas.DataFrame> the airport table that should be placed into the database
    '''

    return airport_data.filter(["id", "airport_code", "name", "type", "latitude_deg", "longitude_deg",
                                "elevation_ft"])


def create_ufo_sightings_table(sightings_data):
    '''
    create_ufo_sightings_table creates the ufo sightings table that should be placed into the database.
    :param sightings_data: <pandas.DataFrame> the cleaned ufo sightings base data
    :return: <pandas.DataFrame> the ufo sightings table that should be placed into the database
    '''

    return sightings_data.filter(["id", "date", "time", "shape", "duration_seconds", "latitude_deg",
                                  "longitude_deg"])


def create_cross_table(table_a, table_b, max_distance):
    '''
    create_cross_table creates a table that has the id of table_a, the id of table_b and the
    distance between the two points in table_a and table_b. No entries are put into the table
    who's distance is not greater than max_distance.
    :param table_a: <pandas.DataFrame> one table with an "id" column, "latitude_deg" column and
        "longitude_deg" column to be crossed with table_b
    :param table_b: <pandas.DataFrame> one table with an "id" column, "latitude_deg" column and
        "longitude_deg" column to be crossed with table_a
    :param max_distance: <int> the maximum distance in miles that two points can be apart from
        each other and still be put into the table
    :return: <pandas.DataFrame> a table which maps all the rows in table_a to all the rows in
        table_b where the distance between the coordinates of the two rows is not greater than
        max_distance
        The columns of the table are "a_id", "b_id" and "distance_miles".
    '''

    # Create the DataFrame for the results to be stored in.
    result = pandas.DataFrame(columns=["a_id", "b_id", "distance_miles"])

    # For every for in table_a:
    for i, a_row in table_a.iterrows():
        a_id = a_row["id"]
        a_coordinates = (a_row["latitude_deg"], a_row["longitude_deg"])

        # For every row in table_b:
        for j, b_row in table_b.iterrows():
            b_id = b_row["id"]
            b_coordinates = (b_row["latitude_deg"], b_row["longitude_deg"])

            distance = great_circle(a_coordinates, b_coordinates).miles

            # If distance is not greater than max_distance, put this record in results.
            if distance <= max_distance:
                result.loc[len(result)] = [a_id, b_id, distance]

        # Print the current progress of this function.
        print("Number %s of %s" % (str(i), str(len(table_a))))

    return result


def create_military_ufo_sightings_mapping_table(military_table, sightings_table, max_distance=10):
    '''
    create_military_ufo_sightings_mapping_table creates a table that maps all the rows in the
    military_table with all the rows in the sightings_table who's distance is not greater than
    max_distance.
    :param military_table: <pandas.DataFrame> one table with an "id" column, "latitude_deg" column and
        "longitude_deg" column that represents the military bases to be crossed with sightings_table
    :param sightings_table: <pandas.DataFrame> one table with an "id" column, "latitude_deg" column and
        "longitude_deg" column that represents the ufo sightings to be crossed with military_table
    :param max_distance: <int> the maximum distance in miles that two points can be apart from
        each other and still be put into the table
        Default Value: 10 miles
    :return: <pandas.DataFrame> a table which maps all the rows in military_table to all the rows in
        sightings_table where the distance between the coordinates of the two rows is not greater than
        max_distance
        The columns of the table are "military_id", "sightings_id" and "distance_miles".
    '''

    result = create_cross_table(military_table, sightings_table, max_distance)
    result = result.rename(columns={"a_id": "military_id", "b_id": "sightings_id"})
    return result


def create_airport_ufo_sightings_mapping_table(airport_table, sightings_table, max_distance=10):
    '''
    create_airport_ufo_sightings_mapping_table creates a table that maps all the rows in the
    airport_table with all the rows in the sightings_table who's distance is not greater than
    max_distance.
    :param airport_table: <pandas.DataFrame> one table with an "id" column, "latitude_deg" column and
        "longitude_deg" column that represents the military bases to be crossed with sightings_table
    :param sightings_table: <pandas.DataFrame> one table with an "id" column, "latitude_deg" column and
        "longitude_deg" column that represents the ufo sightings to be crossed with airport_table
    :param max_distance: <int> the maximum distance in miles that two points can be apart from
        each other and still be put into the table
        Default Value: 10 miles
    :return: <pandas.DataFrame> a table which maps all the rows in airport_table to all the rows in
        sightings_table where the distance between the coordinates of the two rows is not greater than
        max_distance
        The columns of the table are "airport_id", "sightings_id" and "distance_miles".
    '''

    result = create_cross_table(airport_table, sightings_table, max_distance)
    result = result.rename(columns={"a_id": "airport_id", "b_id": "sightings_id"})
    return result


def get_addresses(table):
    '''
    get_addresses gets all the address data out of a DataFrame and puts it into another DataFrame.
    :param table: <pandas.DataFrame> a DataFrame with a "latitude_deg", "longitude_deg", "city",
        "zip_code", "county", "state" and "country" column.
    :return: <pandas.DataFrame> a DataFrame constructed from table that only contains the columns
        "latitude_deg", "longitude_deg", "city", "zip_code", "county", "state" and "country"
    '''

    # Create a DataFrame to store the results.
    result = pandas.DataFrame(columns=["latitude_deg", "longitude_deg", "city", "zip_code",
                                       "county", "state", "country"])

    # For each row in table, input the address data into results.
    for i, row in table.iterrows():
        result.loc[len(result)] = [row["latitude_deg"], row["longitude_deg"], row["city"],
                                   row["zip_code"], row["county"], row["state"], row["country"]]

    return result


def create_address_table(military_data, airport_data, sightings_data):
    '''
    create_address_table creates the addresses table to be placed into the database.
    :param military_data: <pandas.DataFrame> the military data to be placed into the database
    :param airport_data: <pandas.DataFrame> the airport data to be placed into the database
    :param sightings_data: <pandas.DataFrame> the ufo sightings data to be placed into the database
    :return: <pandas.DataFrame> a DataFrame constructed from all the tables that only contains the columns
        "latitude_deg", "longitude_deg", "city", "zip_code", "county", "state" and "country"
    '''

    # Get the address tables for the military, airport and sightings data.
    military_addresses = get_addresses(military_data)
    airport_addresses = get_addresses(airport_data)
    sightings_data = get_addresses(sightings_data)

    # Append all the address tables together into one table.
    addresses = military_addresses.append(airport_addresses)
    addresses = addresses.append(sightings_data)

    return addresses


if __name__ == "__main__":

    print("Creating MilitaryBaseTable.csv")

    # Create the military table and save it out.
    military_data = pandas.read_csv("./CleanData/MilitaryBaseData.csv")
    military_table = create_military_table(military_data)
    military_table.to_csv("./DatabaseTables/MilitaryBaseTable.csv", index=False)


    print("Creating AirportTable.csv")

    # Create the airport table and save it out.
    airport_data = pandas.read_csv("./CleanData/AirportData.csv")
    airport_table = create_airport_table(airport_data)
    airport_table.to_csv("./DatabaseTables/AirportTable.csv", index=False)


    print("Creating UFOSightingData.csv")

    # Create the ufo sightings table and save it out.
    sighting_data = pandas.read_csv("./CleanData/UFOSightingData.csv")
    sighting_table = create_ufo_sightings_table(sighting_data)
    sighting_table.to_csv("./DatabaseTables/UFOSightingTable.csv", index=False)


    print("Creating MilitaryXSightingsTable.csv")

    # Create the military X ufo sightings table and save it out.
    military_X_sightings_table = create_military_ufo_sightings_mapping_table(military_table, sighting_table,
                                                                             max_distance=10)
    military_X_sightings_table.to_csv("./DatabaseTables/MilitaryXSightingsTable.csv", index=False)


    print("Creating AirportXSightingsTable.csv")

    # Create the airport X ufo sightings table and save it out.
    airport_X_sightings_table = create_airport_ufo_sightings_mapping_table(airport_table, sighting_table,
                                                                           max_distance=10)
    airport_X_sightings_table.to_csv("./DatabaseTables/AirportXSightingsTable.csv", index=False)


    print("Creating AddressTable.csv")

    # Create the addresses table and save it out.
    address_table = create_address_table(military_data, airport_data, sighting_data)
    address_table.to_csv("./DatabaseTables/AddressTable.csv", index=False)
