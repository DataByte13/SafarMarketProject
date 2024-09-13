import pymysql

class DBHandler:
    def __init__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.connection = None
        self.cursor = None

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
        """Connect to the MySQL database."""
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
        except pymysql.MySQLError as e:
            print(f"Error connecting to MySQL database: {e}")
            raise

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
        insert_query = """
        INSERT INTO locations (SafarMarketID, Title, Description, Latitude, Longitude, Type, Image, Slug, Rate, RateCount)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            for entry in json_data:
                # Debugging: print the entry being inserted
                print(f"Inserting entry: {entry}")

                # Extracting values with default to avoid NoneType issues
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
                self.cursor.execute(insert_query, values)
            self.connection.commit()
            print(f"{len(json_data)} records inserted into the 'locations' table.")
        except pymysql.MySQLError as e:
            print(f"Error inserting data: {e}")
            self.connection.rollback()
            raise

    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

