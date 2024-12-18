from fastapi import APIRouter
from models.raw_items_model import RawItemModel
from services.raw_items_service import create_raw_item
from utils.response import create_response

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

     