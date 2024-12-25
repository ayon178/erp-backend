from pymongo import MongoClient

# Replace with your MongoDB URI
MONGO_URI = "mongodb+srv://ayonjd178:ayonjd178@cluster0.wqxk9a6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


client = MongoClient(MONGO_URI)
db = client.practice_fastapi
rawItem_collection = db.raw_items
meals_collection = db.meals
feedback_collection = db.feedback_collection
users_collection = db.users_collection
