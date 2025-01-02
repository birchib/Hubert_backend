from pymongo import MongoClient

# Replace with your MongoDB connection string
client = MongoClient('mongodb+srv://birchib:Humphrey2017!@hubert.8g9jd.mongodb.net/')  # Default MongoDB connection

# Select your database
db = client['test']  # Replace with your actual database name

# Select your collection
collection = db['person']  # Replace with your actual collection name

# # Retrieve all documents from the collection
# documents = collection.find()

# # Print the first few documents to inspect the data structure
# for document in documents:
#     print(document)

# Search query
search_query = ""  # Example search query

# Perform the search (case-insensitive)
documents = collection.find({"name": {"$regex": search_query, "$options": "i"}})

# Print the results
for document in documents:
    print(document)


db = client['test']  # Select the database
collection = db['person']  # Select your collection

def insert_into_test_db():
    test_document = {
        'name':'Sabbatical',
        'age': """Sabbatical Leave: To be eligible for sabbatical leave, an employee must have 4 years service, the duration of leave should not exceed 6 months"""
    }
    inserted_id = collection.insert_one(test_document).inserted_id
    print(inserted_id)

insert_into_test_db()

