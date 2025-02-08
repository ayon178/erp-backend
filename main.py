from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware
from fastapi.responses import JSONResponse
from utils.response import create_response
# Routes import
from routes.entry import entry_route
from routes.raw_items_route import raw_items_route
from routes.meals_route import meals_route
from routes.feedback_route import feedback_route
from routes.user_route import user_route

app = FastAPI()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow your frontend's origin
    allow_credentials=True,  # Allow cookies and credentials
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Custom HTTPException Handler
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=create_response(
            status="Error",
            status_code=exc.status_code,
            message=exc.detail,
        ),
    )

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=create_response(
            status="Error",
            status_code=500,
            message="An unexpected error occurred.",
            data={"detail": str(exc)}
        ),
    )

# Validation Error Handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=create_response(
            status="Error",
            status_code=422,
            message="Validation error",
            data={"errors": exc.errors()}
        ),
    )

# Handle routes
app.include_router(entry_route)
app.include_router(raw_items_route)
app.include_router(meals_route)
app.include_router(feedback_route)
app.include_router(user_route)