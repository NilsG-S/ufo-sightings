import atexit
import mysql.connector
import mysql.connector.errorcode
import os

from dotenv import load_dotenv

class DBManager:

    def __init__(self, user_name, password, database=None, host="localhost"):

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

        self.cursor = self.db_connection.cursor()

        if database is not None:
            self.set_database(database)

        atexit.register(self.close_database)

    def reset_cursor(self):
        self.cursor.close()
        self.cursor = self.db_connection.cursor()

    def create_db(self, database_name):
        sql = "CREATE DATABASE %s;" % database_name
        self.cursor.execute(sql)
        self.reset_cursor()

    def delete_database(self, database_name):
        sql = "DROP DATABASE %s;" % database_name
        self.cursor.execute(sql)
        self.reset_cursor()

    def set_database(self, database_name):
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
        sql = "SHOW DATABASES LIKE '%s';" % database_name
        self.cursor.execute(sql)
        answer = len(self.cursor.fetchall()) == 1

        self.reset_cursor()

        return answer

    def create_table(self, table_name, table_schema):
        sql = "CREATE TABLE %s %s;" % (table_name, table_schema)
        self.cursor.execute(sql)

    def insert_csv_into_table(self, table_name, csv_file_path):
        sql = "LOAD DATA LOCAL INFILE '%s' INTO TABLE %s " \
              "FIELDS TERMINATED BY ','" \
              "IGNORE 1 LINES;" % (csv_file_path, table_name)
        self.cursor.execute(sql)
        self.db_connection.commit()

    def close_database(self):
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

# Create airportData table and put the airportData.csv data into the table.
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
db_manager.create_table("airportData", airport_data_schema)
db_manager.insert_csv_into_table("airportData", "/Users/okoepke/Desktop/ufo-sightings/CleanData/AirportData.csv")
