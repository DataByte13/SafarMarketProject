import pymysql
import time
class DBHandler:
    def __init__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.connection = None
        self.cursor = None
        self.insertTracker = 0
    def create_database(self):
         try:
             connection = pymysql.connect(
                 host=self.host,
                 user=self.user,
                 password=self.password,
                 cursorclass=pymysql.cursors.DictCursor
             )
             with connection.cursor() as cursor:
                 cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
             connection.close()
             print(f"Database '{self.database}' created or already exists.")
         except pymysql.MySQLError as e:
             print(f"Error creating database: {e}")
             raise

    def connect(self):
        retries = 10
        while retries > 0 :
            try:
                self.connection = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    cursorclass=pymysql.cursors.DictCursor
                )
                self.cursor = self.connection.cursor()
                print("Database connection established.")
                return 
            except pymysql.MySQLError as e:
                retries -=1 
                print(f"Error connecting to MySQL database: {e} -- {retries} more retries")
                time.sleep(10)
        raise Exception("Could not connect to MySQL after several retries")
    def create_table(self):
        """Create the table if it doesn't exist."""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS locations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            SafarMarketID INT,
            Title VARCHAR(255),
            Description TEXT,
            Latitude FLOAT,
            Longitude FLOAT,
            Type VARCHAR(255),
            Image VARCHAR(255),
            Slug VARCHAR(255),
            Rate FLOAT,
            RateCount INT
        )
        """
        try:
            self.cursor.execute(create_table_query)
            self.connection.commit()
            print("Table 'locations' created or already exists.")
        except pymysql.MySQLError as e:
            print(f"Error creating table: {e}")
            self.connection.rollback()
            raise

    def insert_data(self, json_data):
        """Insert data into the table."""
        select_query = "SELECT COUNT(*) FROM locations WHERE SafarMarketID = %s"
        insert_query = """
        INSERT INTO locations (SafarMarketID, Title, Description, Latitude, Longitude, Type, Image, Slug, Rate, RateCount)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            for entry in json_data:
                values = (
                    entry.get('id', None),
                    entry.get('title', None),
                    entry.get('description', None),
                    entry.get('lat', None),
                    entry.get('lng', None),
                    entry.get('type', None),
                    entry.get('main_image', None),
                    entry.get('slug', None),
                    entry.get('rate', None),
                    entry.get('ratecount', None)
                )
                safar_market_id = entry.get('id', None)
                self.cursor.execute(select_query, (safar_market_id,))
                exists = self.cursor.fetchone()['COUNT(*)']
                if exists == 0 :
                    self.cursor.execute(insert_query, values)
                    self.insertTracker += 1
            self.connection.commit()
        except pymysql.MySQLError as e:
            print(f"Error inserting data: {e}")
            self.connection.rollback()
            raise
    def insert_status(self):
        return self.insertTracker 

    def close(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

