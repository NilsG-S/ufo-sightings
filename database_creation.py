import atexit
import mysql.connector
import mysql.connector.errorcode


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

    def create_table(self, table_sql):
        self.cursor.execute(table_sql)

    def insert_csv_into_table(self, table_name, csv_file_path):
        sql = "LOAD DATA INFILE %s INTO TABLE %s;" % (csv_file_path, table_name)
        self.cursor.execute(sql)
        self.db_connection.commit()

    def close_database(self):
        self.cursor.close()
        self.db_connection.close()
