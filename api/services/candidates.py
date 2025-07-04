from fastapi import HTTPException, status
from sqlalchemy import func, select
from api.models.applications import Applications
from api.models.candidates import Candidates
from api.schemas.applications import ApplicationCreateSchema
from api.schemas.candidates import CandidateDetailedSchema, CandidateUpdateSchema
from api.services.applications import get_applications_list_by_candidate_id
from sqlalchemy.ext.asyncio import AsyncSession


async def get_candidates_list(db: AsyncSession, offset: int = 0, limit: int = 0, skills: list[str] = []):
    query = select(Candidates)

    if skills:
        lowered_skills = [skill.lower() for skill in skills]
        query = query.where(Candidates.skills.op('&&')(lowered_skills))

    query = query.offset(offset=offset).limit(limit=limit)
    result = await db.execute(query)

    return result.scalars().all()


async def get_candidate_by_id(db: AsyncSession, candidate_id: str):
    result = await db.execute(
        select(Candidates).where(Candidates.id == candidate_id)
    )
    candidate = result.scalar_one_or_none()

    if candidate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Candidate not found.')
    
    return candidate

async def create_candidate(db: AsyncSession, candidate: CandidateDetailedSchema):
    new_candidate = Candidates(
        full_name=candidate.full_name.lower(),
        email=str(candidate.email.lower()),
        phone=candidate.phone,
        skills=[skill.lower() for skill in candidate.skills],
    )

    db.add(new_candidate)
    await db.commit()
    await db.refresh(new_candidate)

    return new_candidate

async def update_candidate(db: AsyncSession, candidate_id: str, candidate: CandidateUpdateSchema):
    existing_candidate = await get_candidate_by_id(db, candidate_id)

    for field, value in candidate.model_dump(exclude_unset=True).items():
        if isinstance(value, str):
            value = value.lower()
        elif isinstance(value, list):
            value = [v.lower() if isinstance(v, str) else v for v in value]
        setattr(existing_candidate, field, value)

    await db.commit()
    await db.refresh(existing_candidate)

    return existing_candidate

async def get_applications_by_candidate_id(db: AsyncSession, candidate_id: str):
    existing_candidate = await get_candidate_by_id(db, candidate_id)
    applications = await get_applications_list_by_candidate_id(db, existing_candidate.id)

    return applications
    
async def create_candidate_application(db: AsyncSession, candidate_id: str, application: ApplicationCreateSchema):
    candidate = await get_candidate_by_id(db, candidate_id)

    new_application = Applications(
        candidate_id=candidate.id,
        job_title=func.lower(application.job_title),
        status=application.status,
        applied_at=application.applied_at.replace(tzinfo=None),
    )

    db.add(new_application)
    await db.commit()
    await db.refresh(new_application)

    return new_application