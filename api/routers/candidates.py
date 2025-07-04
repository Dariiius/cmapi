from fastapi import APIRouter, Query
from fastapi.params import Depends
from api.core.config import DEFAULT_PAGINATION_LIMIT
from api.core.db import get_db
from api.schemas.applications import ApplicationCreateSchema, ApplicationSchema
from api.schemas.candidates import CandidateDetailedSchema, CandidateSchema, CandidateUpdateSchema
from api.services.candidates import (
    create_candidate, create_candidate_application, get_applications_by_candidate_id, 
    get_candidates_list, get_candidate_by_id, update_candidate
)
from api.services.users import verify_access_token
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix='/candidates',
    dependencies=[Depends(verify_access_token)], 
    tags=['Candidates']
)


@router.get('/', response_model=list[CandidateSchema])
async def get_candidates(
    offset: int = 0, 
    limit: int = DEFAULT_PAGINATION_LIMIT, 
    skills: list[str] = Query(default=[]),
    db: AsyncSession = Depends(get_db)
):
    candidates = await get_candidates_list(db, offset, limit, skills)
    
    return candidates

@router.get('/{candidate_id}', response_model=CandidateSchema)
async def get_candidate(candidate_id: str, db: AsyncSession = Depends(get_db)):
    candidate = await get_candidate_by_id(db, candidate_id)
    
    return candidate

@router.post('/', response_model=CandidateSchema)
async def post_candidate(candidate: CandidateDetailedSchema, db: AsyncSession = Depends(get_db)):
    new_candidate = await create_candidate(db, candidate)

    return new_candidate

@router.put('/{candidate_id}', response_model=CandidateUpdateSchema)
async def put_candidate(
    candidate_id: str, candidate: CandidateUpdateSchema, db: AsyncSession = Depends(get_db)
):
    updated_candidate = await update_candidate(db, candidate_id, candidate)
    
    return updated_candidate

@router.get('/{candidate_id}/applications', response_model=list[ApplicationSchema])
async def get_candidate_applications(candidate_id: str, db: AsyncSession = Depends(get_db)):
    applications = await get_applications_by_candidate_id(db, candidate_id)

    return applications

@router.post('/{candidate_id}/applications', response_model=ApplicationSchema)
async def post_candidate_application(
    candidate_id: str, application: ApplicationCreateSchema, db: AsyncSession = Depends(get_db)
):
    new_application = await create_candidate_application(db, candidate_id, application)

    return new_application