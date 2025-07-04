from datetime import datetime
from fastapi import HTTPException
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.applications import ApplicationUpdateStatusSchema
from api.services.applications import get_application_by_id, get_applications_list, get_applications_list_by_candidate_id, update_application


# Endpoint tests

# Test for create application
@pytest.mark.anyio
async def test_create_application(async_client, seeded_candidates):
    candidate_id = '3fa85f64-5717-4562-b3fc-2c963f66afa1'
    application_payload = {
        'job_title': 'Software Developer',
        'status': 'applied',
        'applied_at': '2025-07-01T08:52:45.171'
    }
    application_response = await async_client.post(
        f'/candidates/{candidate_id}/applications', json=application_payload
    )
    assert application_response.status_code == 200
    assert application_response.json()['status'] == 'applied'

@pytest.mark.anyio
async def test_update_application(async_client, seeded_candidates, seeded_candidate_application):
    application_id = '3fa85f64-5717-4562-b3fc-2c963f66afb1'
    update_payload = {
        'status': 'interviewing'
    }

    update_response = await async_client.patch(
        f'/applications/{application_id}', json=update_payload
    )
    assert update_response.status_code == 200
    assert update_response.json()['status'] == 'interviewing'


# Service tests

# Test for get_applications_list()
@pytest.mark.anyio
async def test_get_applications_list(
    async_session: AsyncSession, 
    seeded_candidates, 
    seeded_candidate_application
):
    results = await get_applications_list(async_session)

    assert len(results) == 1

# Test for get_application_by_id()
@pytest.mark.anyio
async def test_get_application_by_id(
    async_session: AsyncSession, 
    seeded_candidates, 
    seeded_candidate_application
):
    result = await get_application_by_id(async_session, '3fa85f64-5717-4562-b3fc-2c963f66afb1')

    assert str(result.candidate_id) == '3fa85f64-5717-4562-b3fc-2c963f66afa1'
    assert result.job_title == 'Sofware Developer'
    assert result.status == 'applied'
    assert result.applied_at == datetime.fromisoformat('2025-07-01T17:57:03.364')

# Test for get_applications_list_by_candidate_id()
@pytest.mark.anyio
async def test_get_applications_list_by_candidate_id(
    async_session: AsyncSession, 
    seeded_candidates, 
    seeded_candidate_application
):
    result = await get_applications_list_by_candidate_id(async_session, '3fa85f64-5717-4562-b3fc-2c963f66afa1')

    assert len(result) == 1

# Test for update_application()
@pytest.mark.anyio
async def test_update_application(
    async_session: AsyncSession, 
    seeded_candidates, 
    seeded_candidate_application
):
    payload = ApplicationUpdateStatusSchema(
        status='hired'
    )

    result = await update_application(
        async_session, '3fa85f64-5717-4562-b3fc-2c963f66afb1', payload
    )

    assert result.status == 'hired'

@pytest.mark.anyio
async def test_update_application_not_found(
    async_session: AsyncSession, 
    seeded_candidates, 
    seeded_candidate_application
):
    payload = ApplicationUpdateStatusSchema(
        status='hired'
    )

    with pytest.raises(HTTPException) as exc_info:
        await update_application(
            async_session, '3fa85f64-5717-4562-b3fc-2c963f66afb5', payload
        )

    assert exc_info.value.status_code == 404
