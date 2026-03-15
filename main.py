from fastapi import FastAPI
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from prometheus_client import make_asgi_app

app = FastAPI()

# Configure Prometheus exporter
reader = PrometheusMetricReader()
provider = MeterProvider(metric_readers=[reader])
metrics.set_meter_provider(provider)

meter = metrics.get_meter("fastapi-app")

# Example counter
request_counter = meter.create_counter(
    "http_requests_total",
    description="Total number of HTTP requests",
)

@app.middleware("http")
async def count_requests(request, call_next):
    response = await call_next(request)
    request_counter.add(1, {"method": request.method})
    return response

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI with metrics!"}
    
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
