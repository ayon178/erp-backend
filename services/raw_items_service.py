from typing import Optional, Dict
from pymongo import ASCENDING, DESCENDING
from database.connection import rawItem_collection
from datetime import datetime
from constants.raw_items_constant import SEARCH_FIELDS, FILTER_FIELDS

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


# Function to fetch all raw items with filters
def fetch_all_raw_items(
    search_term: Optional[str],
    page: int,
    limit: int,
    sort_by: str,
    sort_order: str,
    filters: Optional[Dict[str, str]] = None
) -> dict:
    # Pagination calculations
    skip = (page - 1) * limit

    # Search filter
    search_conditions = []
    if search_term:
        search_conditions.append({
            "$or": [
                {field: {"$regex": search_term, "$options": "i"}}
                for field in SEARCH_FIELDS
            ]
        })

    # Additional filters (e.g., addedBy, createdAt)
    if filters:
        for field in FILTER_FIELDS:
            if field in filters:
                if field == "createdAt":
                    try:
                        # Parse mm/dd/yyyy to ISO format
                        start_date = datetime.strptime(filters[field], "%m/%d/%Y")
                        end_date = start_date.replace(hour=23, minute=59, second=59)
                        search_conditions.append({
                            "createdAt": {"$gte": start_date.isoformat(), "$lte": end_date.isoformat()}
                        })
                    except ValueError:
                        raise ValueError("Invalid date format. Use mm/dd/yyyy.")
                else:
                    search_conditions.append({field: filters[field]})

    where_condition = {"$and": search_conditions} if search_conditions else {}

    # Sorting condition
    order = ASCENDING if sort_order == "asc" else DESCENDING
    sort_condition = [(sort_by, order)]

    # Querying the database
    raw_items_cursor = rawItem_collection.find(where_condition).sort(sort_condition).skip(skip).limit(limit)
    raw_items_list = list(raw_items_cursor)

    # Convert ObjectId to string
    for item in raw_items_list:
        item["_id"] = str(item["_id"])

    # Total count for pagination
    total = rawItem_collection.count_documents(where_condition)

    return {
        "meta": {
            "page": page,
            "limit": limit,
            "total": total,
        },
        "data": raw_items_list
    }
