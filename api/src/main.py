from fastapi import FastAPI
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

app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["transactions"])
app.include_router(assistant.router, prefix="/api/v1/assistant", tags=["assistant"])

@app.get("/health")
def health_check():
    return {"status": "operational"}
