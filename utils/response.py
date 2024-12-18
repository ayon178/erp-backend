# utils/response.py
def create_response(status: str, status_code: int, message: str, data: dict = None):
    return {
        "status": status,
        "status-code": status_code,
        "message": message,
        "data": data or None
    }
