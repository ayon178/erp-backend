from database.connection import rawItem_collection
import datetime

# Function to create a new raw item
def create_raw_item(doc: dict) -> dict:
    # Get the current date and time as a string in ISO 8601 format
    current_timestamp = datetime.datetime.now().isoformat()

    # Add the timestamp to the document
    doc["createdAt"] = current_timestamp

    response = rawItem_collection.insert_one(doc)

    return {
        "_id": str(response.inserted_id),
        "title": doc["title"],
        "createdAt": current_timestamp
    }
