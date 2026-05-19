from fastapi import FastAPI, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import random

app = FastAPI()

# Métriques RED
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Nombre total de requêtes HTTP',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'Durée des requêtes HTTP',
    ['method', 'endpoint']
)

@app.middleware("http")
async def metrics_middleware(request, call_next):
    start_time = time.time()
    
    # Simule des erreurs aléatoires (3% du temps)
    if random.random() < 0.03:
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status='500'
        ).inc()
        return Response("Internal Server Error", status_code=500)
    
    response = await call_next(request)
    duration = time.time() - start_time
    
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=str(response.status_code)
    ).inc()
    
    REQUEST_DURATION.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)
    
    return response

@app.get("/")
async def root():
    # Simule une latence variable
    await asyncio.sleep(random.uniform(0.01, 0.5))
    return {"status": "ok", "service": "telemetrie-demo"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

import asyncio
