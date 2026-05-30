from fastapi import FastAPI
from app.api import routes_auth, routes_predict
from app.core.exceptions import register_excetion_handlers
from prometheus_fastapi_instrumentator import Instrumentator
from app.middleware.logging_middleware import LoggingMiddleware

app = FastAPI(title='Car Price Prediction API')

# Link Middleware
app.add_middleware(LoggingMiddleware)

# Link Endpoints
app.include_router(routes_auth.router, tags=['Auth'])
app.include_router(routes_predict.router, tags=['Prediction'])

# Monitoring using Prometheus
Instrumentator().instrument(app).expose(app)

# Add exception handler
register_excetion_handlers(app)