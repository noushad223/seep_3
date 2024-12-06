from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from prometheus_client import Counter, Histogram, generate_latest
from dbfunctions import evaluate_coursework, remain_marks, change_marks
from llm import process_all_courseworks
import logging

app = FastAPI()

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint", "status_code"])
REQUEST_LATENCY = Histogram("http_request_latency_seconds", "Request latency", ["method", "endpoint"])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    method = request.method
    endpoint = request.url.path

    try:
        with REQUEST_LATENCY.labels(method=method, endpoint=endpoint).time():
            response = await call_next(request)

        status_code = response.status_code
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, status_code=str(status_code)).inc()

    except Exception as e:
        logger.error(f"Error during request processing: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    return response

@app.get("/metrics")
async def get_metrics():
    return Response(content=generate_latest(), media_type="text/plain")

@app.post("/submit")
async def submit_data(data: List[str]):
    try:
        module_id, marking_scheme_id = data[0], data[1]
        process_all_courseworks(module_id, marking_scheme_id)
        return {"message": "Courseworks submitted successfully"}
    except Exception as e:
        logger.error(f"Error during coursework submission: {e}")
        raise HTTPException(status_code=400, detail="Failed to submit courseworks")

@app.post("/evaluate")
async def evaluate():
    try:
        result = evaluate_coursework()
        return {"evaluation_result": result}
    except Exception as e:
        logger.error(f"Error during coursework evaluation: {e}")
        raise HTTPException(status_code=500, detail="Failed to evaluate courseworks")

@app.post("/acceptautomark")
async def accept_automark(data: str):
    try:
        change_marks(data)
        return {"message": "Auto marks accepted and updated"}
    except Exception as e:
        logger.error(f"Error during automark acceptance: {e}")
        raise HTTPException(status_code=400, detail="Failed to accept automarks")

@app.post("/denyautomark")
async def deny_automark(data: str):
    try:
        remain_marks(data)
        return {"message": "Auto marks denied and reverted to original"}
    except Exception as e:
        logger.error(f"Error during automark denial: {e}")
        raise HTTPException(status_code=400, detail="Failed to deny automarks")