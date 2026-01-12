import pytest
from unittest.mock import AsyncMock, patch
from api.src.main import app
from httpx import AsyncClient, ASGITransport

@pytest.fixture
def anyio_backend():
    return 'asyncio'

@pytest.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
