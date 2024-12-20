from fastapi import APIRouter, Query, HTTPException
from typing import Optional, Dict
from models.raw_items_model import RawItemModel
from services.raw_items_service import create_raw_item
from utils.response import create_response
from services.raw_items_service import fetch_all_raw_items, edit_raw_item

raw_items_route = APIRouter()

# Route to create a new raw item
@raw_items_route.post("/new/raw-item")
def new_raw_item(doc: RawItemModel):
    response_data = create_raw_item(doc.dict())
    return create_response(
        status="Ok",
        status_code=201,
        message="Raw item created successfully",
        data=response_data
    )

# Get all raw items
@raw_items_route.get("/raw-items")
def get_all_raw_items(
    search_term: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    sort_by: Optional[str] = "date",
    sort_order: Optional[str] = "desc",
    addedBy: Optional[str] = None,
    created_at: Optional[str] = None
):
    # Prepare filters dictionary
    filters: Dict[str, str] = {}
    if addedBy:
        filters["addedBy"] = addedBy
    if created_at:
        filters["createdAt"] = created_at

    # Fetch raw items using the service function
    response_data = fetch_all_raw_items(search_term, page, limit, sort_by, sort_order, filters)

    # Return the standardized response
    return create_response(
        status="Ok",
        status_code=200,
        message="Raw items fetched successfully",
        data=response_data
    )
     
# Update raw item
@raw_items_route.put("/update/raw-item/{item_id}")
def update_raw_item(item_id: str, updates: Dict):
    try:
        response_data = edit_raw_item(item_id, updates)
        return create_response(
            status="Ok",
            status_code=200,
            message="Raw item updated successfully",
            data=response_data
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))