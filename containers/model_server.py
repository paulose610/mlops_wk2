import os
import time
import json
import logging
import mlflow
import pandas as pd
from fastapi import FastAPI, Request, HTTPException, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# ---------- OpenTelemetry Imports ----------
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter

# ---------- OpenTelemetry Setup ----------
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
span_processor = BatchSpanProcessor(CloudTraceSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)

# ---------- Structured JSON Logging ----------
logger = logging.getLogger("iris-ml-service")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()

formatter = logging.Formatter(json.dumps({
    "severity": "%(levelname)s",
    "message": "%(message)s",
    "timestamp": "%(asctime)s"
}))
handler.setFormatter(formatter)
logger.addHandler(handler)

# ---------- FastAPI Initialization ----------
app = FastAPI(title="🌸 Iris Classifier API with Observability")

# ---------- MLflow Model Setup ----------
MLFLOW_TRACKING_URI = "http://35.184.91.21:8100"
MODEL_NAME = os.getenv("MODEL_NAME", "IRIS-classifier-dt")
MODEL_VERSION = os.getenv("MODEL_VERSION", "1")

model = None
app_state = {"is_ready": False, "is_alive": True}

@app.on_event("startup")
async def startup_event():
    """Simulate model load and set readiness flag."""
    global model
    try:
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        model_uri = f"models:/{MODEL_NAME}/{MODEL_VERSION}"
        model = mlflow.sklearn.load_model(model_uri)
        logger.info(f"Loaded model '{MODEL_NAME}' version {MODEL_VERSION}")
        app_state["is_ready"] = True
    except Exception as e:
        logger.exception(json.dumps({
            "event": "model_load_error",
            "error": str(e)
        }))
        raise HTTPException(status_code=500, detail="Failed to load model")

# ---------- Health Probes ----------
@app.get("/live_check", tags=["Probe"])
async def liveness_probe():
    if app_state["is_alive"]:
        return {"status": "alive"}
    return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.get("/ready_check", tags=["Probe"])
async def readiness_probe():
    if app_state["is_ready"]:
        return {"status": "ready"}
    return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

# ---------- Request Timing Middleware ----------
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = round((time.time() - start_time) * 1000, 2)
    response.headers["X-Process-Time-ms"] = str(duration)
    return response

# ---------- Global Exception Handler ----------
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    span = trace.get_current_span()
    trace_id = format(span.get_span_context().trace_id, "032x")
    logger.exception(json.dumps({
        "event": "unhandled_exception",
        "trace_id": trace_id,
        "path": str(request.url),
        "error": str(exc)
    }))
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "trace_id": trace_id},
    )

# ---------- Pydantic Schema ----------
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# ---------- Root Endpoint ----------
@app.get("/")
def root():
    return {"model": MODEL_NAME, "version": MODEL_VERSION, "status": "running"}

# ---------- Prediction Endpoint ----------
@app.post("/predict")
async def predict(input: IrisInput, request: Request):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded.")
    
    with tracer.start_as_current_span("model_inference") as span:
        start_time = time.time()
        trace_id = format(span.get_span_context().trace_id, "032x")

        try:
            input_data = input.dict()
            input_df = pd.DataFrame([input_data])
            prediction = model.predict(input_df)[0]
            latency = round((time.time() - start_time) * 1000, 2)

            log_entry = {
                "event": "prediction",
                "trace_id": trace_id,
                "input": input_data,
                "prediction": str(prediction),
                "latency_ms": latency,
                "status": "success"
            }
            logger.info(json.dumps(log_entry))

            return {"predicted_species": prediction, "trace_id": trace_id}

        except Exception as e:
            logger.exception(json.dumps({
                "event": "prediction_error",
                "trace_id": trace_id,
                "error": str(e)
            }))
            raise HTTPException(status_code=500, detail="Prediction failed")
