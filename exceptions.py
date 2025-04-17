from fastapi import HTTPException

class ExternalAPIError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=503, detail=f"External API Error: {detail}")

class DataProcessingError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=f"Data Processing Error: {detail}")

class InternalServerError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=f"Internal Server Error: {detail}")
