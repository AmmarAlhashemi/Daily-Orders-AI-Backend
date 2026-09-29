from fastapi import FastAPI, HTTPException

from schemas import ParseOrdersRequest, SmartSplitRequest
from gemini_service import parse_raw_orders, smart_split_data
from exceptions import PrimaryModelError, FallbackModelError


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Backend is running!"}


@app.post("/parse-orders")
def parse_orders(request: ParseOrdersRequest):
    try:
        return parse_raw_orders(
            request.raw_data,
            request.use_fallback
        )

    except PrimaryModelError as error:
        raise HTTPException(
            status_code=503,
            detail={
                "code": "PRIMARY_MODEL_FAILED",
                "message": str(error)
            }
        )

    except FallbackModelError as error:
        raise HTTPException(
            status_code=503,
            detail={
                "code": "FALLBACK_MODEL_FAILED",
                "message": str(error)
            }
        )


@app.post("/smart-split")
def smart_split(request: SmartSplitRequest):
    try:
        return smart_split_data(
            request.excel_data,
            request.use_fallback
        )

    except PrimaryModelError as error:
        raise HTTPException(
            status_code=503,
            detail={
                "code": "PRIMARY_MODEL_FAILED",
                "message": str(error)
            }
        )

    except FallbackModelError as error:
        raise HTTPException(
            status_code=503,
            detail={
                "code": "FALLBACK_MODEL_FAILED",
                "message": str(error)
            }
        )
