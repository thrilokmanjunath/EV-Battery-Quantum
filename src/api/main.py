import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from .routes import router
from .websockets import ws_router
from .endpoints import router as sse_router
# Import metrics to ensure they are registered
from . import metrics

app = FastAPI(title="EV Battery Quantum Optimization API")

# Configure CORS
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")
origins = allowed_origins_env.split(",") if allowed_origins_env else []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(router)
app.include_router(ws_router)
app.include_router(sse_router)

# Add prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
