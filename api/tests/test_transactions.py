import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_create_transaction_success(async_client):
    transaction_data = {
        "user_id": "user123",
        "amount": 100,
        "type": "deposit"
    }
    idempotency = "unique-id-123"

    with patch('api.src.infrastructure.api.routers.transactions.MongoTransactionRepository') as MockRepo:
        mock_repo_instance = MockRepo.return_value
        mock_repo_instance.get_by_id = AsyncMock(return_value=None)
        mock_repo_instance.save = AsyncMock(return_value=None)

        response = await async_client.post(f"/api/v1/transactions/create/{idempotency}", json=transaction_data)

        assert response.status_code == 200
        assert response.json()["id"] == idempotency
        assert response.json()["data"]["user_id"] == "user123"

@pytest.mark.asyncio
async def test_create_transaction_duplicate(async_client):
    transaction_data = {
        "user_id": "user123",
        "amount": 100,
        "type": "deposit"
    }
    idempotency = "unique-id-123"

    with patch('api.src.infrastructure.api.routers.transactions.MongoTransactionRepository') as MockRepo:
        mock_repo_instance = MockRepo.return_value
        # Simulate that the transaction already exists
        mock_repo_instance.get_by_id = AsyncMock(return_value={"id": idempotency})

        response = await async_client.post(f"/api/v1/transactions/create/{idempotency}", json=transaction_data)

        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]

@pytest.mark.asyncio
async def test_async_process_success(async_client):
    idempotency = "unique-id-123"
    request_data = {"id": idempotency}
    
    mock_transaction = AsyncMock()
    mock_transaction.idempotency_key = idempotency
    mock_transaction.user_id = "user123"
    mock_transaction.amount = 100
    mock_transaction.type = "deposit"
    mock_transaction.status = "pending"

    with patch('api.src.infrastructure.api.routers.transactions.MongoTransactionRepository') as MockRepo, \
         patch('api.src.infrastructure.api.routers.transactions.RabbitMQBroker') as MockBroker:
        
        mock_repo_instance = MockRepo.return_value
        mock_repo_instance.get_by_id = AsyncMock(return_value=mock_transaction)
        
        mock_broker_instance = MockBroker.return_value
        mock_broker_instance.publish = AsyncMock(return_value=None)

        response = await async_client.post("/api/v1/transactions/async-process", json=request_data)

        assert response.status_code == 200
        assert response.json()["message"] == "Transaction sent to processing queue"
        mock_broker_instance.publish.assert_called_once()
