from pymongo import MongoClient

class AWSDocumentDBConnector:
    def __init__(self, username, password, host, port, database):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.client = None
        self.db = None

    def connect(self):
        try:
            # Create the connection string
            connection_string = f"mongodb+srv://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}?ssl=true&ssl_cert_reqs=CERT_NONE"

            # Connect to AWS DocumentDB
            self.client = MongoClient(connection_string)
            self.db = self.client[self.database]

            print("Connected to AWS DocumentDB")
        except Exception as e:
            print(f"Error connecting to AWS DocumentDB: {e}")

    def disconnect(self):
        if self.client:
            self.client.close()
            print("Disconnected from AWS DocumentDB")

    def example_query(self):
        if self.db:
            # Example query: Print the names of all collections in the current database
            collections = self.db.list_collection_names()
            print("Collections in the database:")
            for collection in collections:
                print(collection)
        else:
            print("Not connected to the database. Call connect() first.")

# Example usage:
# connector = AWSDocumentDBConnector(
#     username="your_username",
#     password="your_password",
#     host="your_documentdb_cluster_endpoint",
#     port=27017,  # Default MongoDB port
#     database="your_database_name"
# )

# connector.connect()
# connector.example_query()
# connector.disconnect()
