from datetime import datetime
import os
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from api.core.db import Base, get_db
from api.models.applications import Applications
from api.models.candidates import Candidates
from api.schemas.users import AccessTokenDataSchema
from api.services.users import verify_access_token
from main import app


DATABASE_URL = os.getenv('DATABASE_URL')

@pytest.fixture
def anyio_backend():
    return 'asyncio'

@pytest.fixture(scope='function')
async def test_engine():
    engine = create_async_engine(DATABASE_URL, echo=False)
    yield engine
    await engine.dispose()

@pytest.fixture(scope='function', autouse=True)
async def setup_database(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope='function')
async def async_session(test_engine):
    async_session_factory = async_sessionmaker(bind=test_engine, expire_on_commit=False)
    async with async_session_factory() as session:
        yield session

@pytest.fixture
async def async_client(async_session):
    async def override_get_db():
        yield async_session

    async def override_verify_access_token():
        return AccessTokenDataSchema(email='admin@example.com')

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[verify_access_token] = override_verify_access_token

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

@pytest.fixture
async def seeded_candidates(async_session):
    candidate_1 = Candidates(
        id='3fa85f64-5717-4562-b3fc-2c963f66afa1',
        full_name='Jane Doe',
        email='janed@example.com',
        phone='1234567890',
        skills=['python', 'fastapi', 'sqlalchemy']
    )
    candidate_2 = Candidates(
        id='3fa85f64-5717-4562-b3fc-2c963f66afa2',
        full_name='Jay Doe',
        email='jayd@example.com',
        phone='0987654321',
        skills=['javascript', 'react']
    )
    async_session.add_all([candidate_1, candidate_2])
    await async_session.commit()

    return [candidate_1, candidate_2]


@pytest.fixture
async def seeded_candidate_application(async_session):
    application = Applications(
        id='3fa85f64-5717-4562-b3fc-2c963f66afb1',
        candidate_id='3fa85f64-5717-4562-b3fc-2c963f66afa1',
        job_title='Sofware Developer',
        status='applied',
        applied_at=datetime.fromisoformat('2025-07-01T17:57:03.364')
    )

    async_session.add(application)
    await async_session.commit()

    return application