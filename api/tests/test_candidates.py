import pytest
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.models.candidates import Candidates
from api.schemas.applications import ApplicationCreateSchema
from api.schemas.candidates import CandidateDetailedSchema, CandidateUpdateSchema
from api.services.candidates import (
    create_candidate, create_candidate_application, get_applications_by_candidate_id, 
    get_candidate_by_id, get_candidates_list, update_candidate
)


# Endpoint tests

# Test for create candidate
@pytest.mark.anyio
async def test_create_candidate(async_client):
    payload = {
        'full_name': 'John D. One',
        'email': 'jdone@gmail.com',
        'phone': '955888811',
        'skills': ['html', 'python', 'javascript', 'react']
    }
    response = await async_client.post('/candidates/', json=payload)
    
    assert response.status_code == 200


# Service tests

# Tests for get_candidates_list()
@pytest.mark.anyio
async def test_get_candidates_list(async_session: AsyncSession, seeded_candidates):
    results = await get_candidates_list(async_session, 0, 10, [])

    assert len(results) == 2
    assert all(isinstance(c, Candidates) for c in results)

    
@pytest.mark.anyio
async def test_get_candidates_list_filter_skills(async_session: AsyncSession, seeded_candidates):
    results = await get_candidates_list(async_session, 0, 10, ['react'])

    assert len(results) == 1
    assert results[0].email == 'jayd@example.com'


@pytest.mark.anyio
async def test_get_candidates_list_offset_limit(async_session: AsyncSession, seeded_candidates):
    results = await get_candidates_list(async_session, 1, 1, [])

    assert len(results) == 1
    assert results[0].email == 'jayd@example.com'

# Tests for get_candidate_by_id()
@pytest.mark.anyio
async def test_get_candidate_by_id(async_session: AsyncSession, seeded_candidates):
    results = await get_candidate_by_id(async_session, '3fa85f64-5717-4562-b3fc-2c963f66afa2')

    assert results.email == 'jayd@example.com'

@pytest.mark.anyio
async def test_get_candidate_by_id_not_found(async_session: AsyncSession, seeded_candidates):
    with pytest.raises(HTTPException) as exc_info:
        await get_candidate_by_id(async_session, '3fa85f64-5717-4562-b3fc-2c963f66afa3')

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == 'Candidate not found.'
    
# Tests for create_candidate()
@pytest.mark.anyio
async def test_create_candidate(async_session: AsyncSession):
    candidate = CandidateDetailedSchema(
        full_name='John Done',
        email='jdone@example.com',
        phone='867188822',
        skills=['nodejs', 'angular', 'react native']
    )

    new_candidate = await create_candidate(async_session, candidate)

    assert new_candidate.id is not None
    assert new_candidate.full_name == 'john done'
    assert new_candidate.email == 'jdone@example.com'
    assert new_candidate.phone == '867188822'
    assert sorted(new_candidate.skills) == ['angular', 'nodejs', 'react native']

# Tests for update_candidate()
@pytest.mark.anyio
async def test_update_candidate(async_session: AsyncSession, seeded_candidates):
    payload = CandidateUpdateSchema(
        full_name='Jane Does',
        email='jdoes@example.com',
        phone='790988800',
        skills=['javascript', 'react', 'ruby']
    )

    updated_candidate = await update_candidate(
        async_session, 
        '3fa85f64-5717-4562-b3fc-2c963f66afa1', 
        payload
    )

    assert updated_candidate.full_name == 'jane does'
    assert updated_candidate.email == 'jdoes@example.com'
    assert updated_candidate.phone == '790988800'
    assert sorted(updated_candidate.skills) == ['javascript', 'react', 'ruby']

# Tests for get_applications_by_candidate_id()
@pytest.mark.anyio
async def test_get_applications_by_candidate_id(
    async_session: AsyncSession, 
    seeded_candidates, 
    seeded_candidate_application
):
    results = await get_applications_by_candidate_id(
        async_session, 
        '3fa85f64-5717-4562-b3fc-2c963f66afa1'
    )

    assert len(results) == 1
    assert str(results[0].id) == '3fa85f64-5717-4562-b3fc-2c963f66afb1'
    assert results[0].status == 'applied'
    assert results[0].applied_at == datetime.fromisoformat('2025-07-01T17:57:03.364')

@pytest.mark.anyio
async def test_get_applications_by_candidate_id_no_result(
    async_session: AsyncSession, 
    seeded_candidates, 
):
    results = await get_applications_by_candidate_id(
        async_session, 
        '3fa85f64-5717-4562-b3fc-2c963f66afa1'
    )

    assert len(results) == 0

# Test for create_candidate_application()
@pytest.mark.anyio
async def test_create_candidate_application(async_session: AsyncSession, seeded_candidates):
    application = ApplicationCreateSchema(
        job_title='Web Developer',
        status='applied',
        applied_at=datetime.fromisoformat('2025-07-01T17:57:03.364')
    )

    new_application = await create_candidate_application(
        async_session, 
        '3fa85f64-5717-4562-b3fc-2c963f66afa1',
        application
    )

    assert new_application.id is not None
    assert new_application.job_title == 'web developer'
    assert new_application.status == 'applied'
    assert new_application.applied_at == datetime.fromisoformat('2025-07-01T17:57:03.364')

@pytest.mark.anyio
async def test_create_candidate_application_candidate_not_found(
    async_session: AsyncSession, 
    seeded_candidates
):
    application = ApplicationCreateSchema(
        job_title='Web Developer',
        status='applied',
        applied_at=datetime.fromisoformat('2025-07-01T17:57:03.364')
    )

    with pytest.raises(HTTPException) as exc_info:
        await create_candidate_application(
            async_session, 
            '3fa85f64-5717-4562-b3fc-2c963f66afa5',
            application
        )

    assert exc_info.value.status_code == 404