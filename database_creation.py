import atexit
import mysql.connector
import mysql.connector.errorcode
import os

from dotenv import load_dotenv


class DBManager:
    '''
    DBManager connects to a mariadb database in order to manage it.
    '''

    def __init__(self, user_name, password, database=None, host="localhost"):
        '''
        :param user_name: <str> a valid user name to login to the database with
        :param password: <str> a valid password for the user name passed in to login to the
            database with
        :param database: <str|None> the name of the database that is wished to be managed or None if there
            is not a set database to set.
            Default: None
        :param host: <str> the address of the database to connect with
            Default: "localhost"
        '''

        # Try to connect to the database.
        try:
            self.db_connection = mysql.connector.connect(host=host, user=user_name, password=password)

        except mysql.connector.Error as error:
            if error.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
                raise error

            elif error.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
                raise error

            else:
                print(error)
                raise error

        # Connect a cursor to the database.
        self.cursor = self.db_connection.cursor()

        # If there is a database passed to connect to, connect to it.
        if database is not None:
            self.set_database(database)

        # Register the self.close_database method to be ran when this object is deleted.
        atexit.register(self.close_database)

    def reset_cursor(self):
        '''
        reset_cursor resets self.cursor to a new cursor object.
        :return:None
        '''

        self.cursor.close()
        self.cursor = self.db_connection.cursor()

    def create_db(self, database_name):
        '''
        create_db creates a new database of name database_name.
        :param database_name: <str> the name to call the new database
        :return: None
        '''

        sql = "CREATE DATABASE %s;" % database_name
        self.cursor.execute(sql)
        self.reset_cursor()

    def delete_database(self, database_name):
        '''
        delete_database deletes the database with the name stored in database_name.
        :param database_name: <str> the name of the database to delete.
        :return: None
        '''

        sql = "DROP DATABASE %s;" % database_name
        self.cursor.execute(sql)
        self.reset_cursor()

    def set_database(self, database_name):
        '''
        set_database sets the working database to the database named database_name.
        :param database_name: <str> the name of the database to set the working database to.
        :return: None
        '''

        # Try to set the databse to database_name.
        try:
            self.db_connection.database = database_name

        except mysql.connector.Error as error:
            if error.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                print("Database named %s does not exist." % database_name)
                raise error

            else:
                print(error)
                raise error

        else:
            self.reset_cursor()

    def database_exists(self, database_name):
        '''
        database_exists checks to see if the database database_name exists.
        :param database_name: <str> the database name to check if it exists
        :return: <boolean> True if the database exists and False otherwise
        '''

        sql = "SHOW DATABASES LIKE '%s';" % database_name
        self.cursor.execute(sql)
        answer = len(self.cursor.fetchall()) == 1

        self.reset_cursor()

        return answer

    def create_table(self, table_name, table_schema):
        '''
        create_table creates the table table_name with the table schema table_schema.
        :param table_name: <str> the table name to create
        :param table_schema: <str> the table schema to use to create the table
        :return: None
        '''

        sql = "CREATE TABLE %s %s;" % (table_name, table_schema)
        self.cursor.execute(sql)

    def insert_csv_into_table(self, table_name, csv_file_path):
        '''
        insert_csv_into_table inserts the csv file located at csv_file_path in to the table
        named table_name.
        :param table_name: <str> the table name to insert the csv data into
        :param csv_file_path: <str> the file path to where the csv file is located
        :return: None
        '''

        sql = "LOAD DATA LOCAL INFILE '%s' INTO TABLE %s " \
              "FIELDS TERMINATED BY ','" \
              "IGNORE 1 LINES;" % (csv_file_path, table_name)
        self.cursor.execute(sql)
        self.db_connection.commit()

    def close_database(self):
        '''
        close_database closes the connection to the database.
        :return: None
        '''

        self.cursor.close()
        self.db_connection.close()


# Load the environment file for environment variable.
load_dotenv("./.env")

# Get the database username and password from the .env file.
db_user_name = os.getenv("DB_USER_NAME")
db_password = os.getenv("DB_PASSWORD")

db_name = "ufo"

# Create a database manager to start editing the database.
db_manager = DBManager(user_name=db_user_name, password=db_password)

# If a database named that vale stored in db_name already exists, delete it.
if db_manager.database_exists(db_name):
    db_manager.delete_database(db_name)

# Create a database named the value stored in db_name and set the working database to this database.
db_manager.create_db(db_name)
db_manager.set_database(db_name)

# Create AirportData table and put the airportData.csv data into the table.
airport_data_schema = "(" \
                      "id int(8) NOT NULL," \
                      "airport_code varchar(40)," \
                      "type varchar(40)," \
                      "name varchar(40)," \
                      "latitude_deg double(9, 6)," \
                      "longitude_deg double(9, 6)," \
                      "elevation int(6)," \
                      "country varchar(40)," \
                      "state varchar(40)," \
                      "city varchar(40)," \
                      "zip_code int(5)," \
                      "PRIMARY KEY (id)" \
                      ")"
db_manager.create_table("AirportData", airport_data_schema)
db_manager.insert_csv_into_table("AirportData", "/Users/okoepke/Desktop/ufo-sightings/CleanData/AirportData.csv")

# Create MeteoriteData table and put the airportData.csv data into the table.
meteorite_data_schema = "(" \
                        "name varchar(40) NOT NULL," \
                        "id int(5) NOT NULL," \
                        "mass_grams double(9, 1)," \
                        "date date," \
                        "time time," \
                        "country varchar(40)," \
                        "zip_code int(6)," \
                        "PRIMARY KEY (id)" \
                        ")"
db_manager.create_table("MeteoriteData", meteorite_data_schema)
db_manager.insert_csv_into_table("MeteoriteData", "/Users/okoepke/Desktop/ufo-sightings/CleanData/MeteoriteData.csv")

# Create MilitaryBaseData table and put the airportData.csv data into the table.
military_base_data_schema = "(" \
                            "id int(8) NOT NULL," \
                            "name varchar(40)," \
                            "type varchar(40)," \
                            "state varchar(40)," \
                            "longitude_deg double(9, 6)," \
                            "latitude_deg double(9, 6)," \
                            "zip_code int(5)," \
                            "PRIMARY KEY (id)" \
                            ")"
db_manager.create_table("MilitaryBaseData", military_base_data_schema)
db_manager.insert_csv_into_table("MilitaryBaseData", "/Users/okoepke/Desktop/ufo-sightings/CleanData/MilitaryBaseData.csv")

# Create UFOSightingData table and put the airportData.csv data into the table.
ufo_sighting_data_schema = "(" \
                           "date date," \
                           "time time," \
                           "city varchar(40)," \
                           "state varchar(40)," \
                           "country varchar(40)," \
                           "zip_code int(5)," \
                           "shape varchar(40)," \
                           "duration_seconds int(9)," \
                           "latitude_deg double(9, 6)," \
                           "longitude_deg double(9, 6)" \
                           ")"
db_manager.create_table("UFOSightingData", ufo_sighting_data_schema)
db_manager.insert_csv_into_table("UFOSightingData", "/Users/okoepke/Desktop/ufo-sightings/CleanData/UFOSightingData.csv")
