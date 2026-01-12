from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from api.src.infrastructure.api.routers import transactions
from api.src.infrastructure.api.routers import assistant

app = FastAPI(title="Payments API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción deberías restringir esto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def security_middleware(request: Request, call_next):
    # Exclude health check and docs
    if request.url.path == "/health" or request.url.path.startswith("/docs") or request.url.path.startswith("/openapi.json"):
        return await call_next(request)

    # Exclude websocket path
    if request.url.path == "/api/v1/transactions/ws":
        return await call_next(request)

    # Allow OPTIONS for CORS preflight
    if request.method == "OPTIONS":
        return await call_next(request)

    if "Authorization" not in request.headers:
        return JSONResponse(status_code=401, content={"detail": "Authorization header missing"})

    return await call_next(request)

app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["transactions"])
app.include_router(assistant.router, prefix="/api/v1/assistant", tags=["assistant"])

@app.get("/health")
def health_check():
    return {"status": "operational"}
