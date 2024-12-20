from datetime import datetime
from pymongo import ASCENDING, DESCENDING
from typing import Optional, Dict
from database.connection import meals_collection, rawItem_collection
from database.connection import meals_collection
from bson import ObjectId
from constants.meals_constant import SEARCH_FIELDS, FILTER_FIELDS


def create_meals(doc: dict) -> dict:
    """
    Create a new meal document in the database if the name is unique.

    :param doc: The meal document to be inserted.
    :return: A dictionary containing the inserted document ID and metadata.
    """
    # Check if a meal with the same name already exists
    existing_meal = meals_collection.find_one({"name": doc["name"]})
    if existing_meal:
        raise ValueError(f"A meal with the name '{doc['name']}' already exists.")

    # Get the current timestamp
    current_timestamp = datetime.now().isoformat()
    doc["createdAt"] = current_timestamp

    # Insert the document into the database
    response = meals_collection.insert_one(doc)

    # Return the response data
    return {
        "_id": str(response.inserted_id),
        "title": doc["name"],
        "createdAt": current_timestamp
    }


def fetch_all_meals(
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

    # Additional filters (e.g., rawItem, createdAt)
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
    meals_cursor = meals_collection.find(where_condition).sort(sort_condition).skip(skip).limit(limit)
    meals_list = list(meals_cursor)

    # Populate rawItem array
    for meal in meals_list:
        meal["_id"] = str(meal["_id"])
        populated_raw_items = []
        for raw_item_id in meal.get("rawItem", []):
            # Ensure raw_item_id is converted to ObjectId
            if isinstance(raw_item_id, str):
                try:
                    raw_item_id = ObjectId(raw_item_id)
                except Exception:
                    continue

            raw_item = rawItem_collection.find_one({"_id": raw_item_id})
            if raw_item:
                raw_item["_id"] = str(raw_item["_id"])
                populated_raw_items.append(raw_item)
        meal["rawItem"] = populated_raw_items

    # Total count for pagination
    total = meals_collection.count_documents(where_condition)

    return {
        "meta": {
            "page": page,
            "limit": limit,
            "total": total,
        },
        "data": meals_list
    }
