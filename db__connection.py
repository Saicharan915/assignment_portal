import pymongo

# MongoDB connection details
MONGO_URL = 'mongodb://localhost:27017'
client = pymongo.MongoClient(MONGO_URL)
db = client['assignment_portal']  # Database name
