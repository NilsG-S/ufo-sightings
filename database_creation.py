import mysql.connector


class DBManager:

    def __init__(self, user_name, password, host="localhost"):
        self.db_connection = mysql.connector.connect(host=host, user=user_name, password=password)
        self.cursor = self.db_connection.cursor()

    def create_db(self, database_name):
        sql = "CREATE DATABASE %s;" % database_name
        self.cursor.execute(sql)

    def create_table(self):
        pass

    def insert_csv_into_table(self):
        pass
