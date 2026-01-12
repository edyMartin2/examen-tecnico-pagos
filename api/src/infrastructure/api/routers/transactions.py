from fastapi import APIRouter, HTTPException
from api.src.application.dtos.transaction import TransactionType
from api.src.domain.models.transaction import Transaction
from api.src.infrastructure.adapters.mongo.transaction_repository import MongoTransactionRepository
from api.src.infrastructure.adapters.rabbitmq.broker import RabbitMQBroker
from api.src.application.dtos.async_process import TransactionAsyncProcessRequest
from fastapi import WebSocket, WebSocketDisconnect
import asyncio

router = APIRouter()

@router.post("/create/{idempotency_id}")
async def create_transaction(idempotency_id: str, transaction: TransactionType):
    repository = MongoTransactionRepository()
    
    # Validamos si ya existe una transacción con ese ID
    existing_transaction = await repository.get_by_id(idempotency_id)
    if existing_transaction:
        raise HTTPException(status_code=409, detail="Transaction with ID : "+ idempotency_id + " already exists")

    new_transaction = Transaction(
        user_id=transaction.user_id,
        amount=transaction.amount,
        type=transaction.type,
        idempotency_key=idempotency_id
    )
    
    await repository.save(new_transaction)
    
    return {"message": "Transaction created successfully", "id": idempotency_id, "data": transaction}

@router.post("/async-process")
async def transaction_async_process(request: TransactionAsyncProcessRequest):
    repository = MongoTransactionRepository()
    broker = RabbitMQBroker()
    
    transaction = await repository.get_by_id(request.id)
    
    if not transaction:
        raise HTTPException(status_code=404, detail=f"Transaction with ID {request.id} not found")

    message = {
        "transaction_id": transaction.idempotency_key,
        "user_id": transaction.user_id,
        "amount": transaction.amount,
        "type": transaction.type,
        "status": transaction.status
    }
    
    # Publicamos en la cola 'transaction_processing_queue'
    await broker.publish("transaction_processing_queue", message)

    return {"message": "Transaction sent to processing queue", "data": transaction}


@router.websocket("/ws")
async def websocket_transaction_status(websocket: WebSocket):
    await websocket.accept()
    repository = MongoTransactionRepository()
    try:
        while True:
            transactions = await repository.get_all()
            data = [
                {
                    "user_id": t.user_id,
                    "amount": t.amount,
                    "type": t.type,
                    "idempotency_key": t.idempotency_key,
                    "status": t.status
                } 
                for t in transactions
            ]
            
            await websocket.send_json({"data": data})      
            await asyncio.sleep(1)
            
    except WebSocketDisconnect:
        print(f"Cliente desconectado del websocket")
