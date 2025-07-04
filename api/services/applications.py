from fastapi import HTTPException, status
from sqlalchemy import select
from api.models.applications import Applications
from api.schemas.applications import ApplicationUpdateStatusSchema
from sqlalchemy.ext.asyncio import AsyncSession


async def get_applications_list(db: AsyncSession):
    results = await db.execute(select(Applications))

    return results.scalars().all()

async def get_application_by_id(db: AsyncSession, application_id: str):
    result = await db.execute(
        select(Applications).where(Applications.id == application_id)
    )
    application = result.scalar_one_or_none()

    if application is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Application not found.')
    
    return application
    
async def get_applications_list_by_candidate_id(db: AsyncSession, candidate_id: str):
    result = await db.execute(
        select(Applications).where(Applications.candidate_id == candidate_id)
    )
    return result.scalars().all()

async def update_application(
        db: AsyncSession, application_id: str, status: ApplicationUpdateStatusSchema
):
    existing_application = await get_application_by_id(db, application_id)

    for field, value in status.model_dump(exclude_unset=True).items():
        setattr(existing_application, field, value)

    await db.commit()
    await db.refresh(existing_application)

    return existing_application
