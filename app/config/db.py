import time
from pymongo import MongoClient

MAX_ATTEMPTS = 5
attempts = 0
# Try to establish a connection to the MongoDB database using the MongoClient() method
# and passing in a connection string.
while attempts < MAX_ATTEMPTS:
    try:
        client = MongoClient("mongodb+srv://wolfandbadger:adminpass@wolfandbadger.z7uhqro.mongodb.net/?retryWrites=true&w=majority")
        db = client.test
        break
    except ConnectionError:
        # If a connection cannot be established, increment the attempt counter and sleep for 1 second before trying
        # again.
        attempts += 1
        time.sleep(1)
else:
    # Raise a ConnectionError if the maximum number of attempts is reached.
    raise ConnectionError("Could not establish connection to MongoDB")

