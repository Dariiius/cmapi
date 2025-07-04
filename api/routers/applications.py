from fastapi import APIRouter
from fastapi.params import Depends
from api.core.db import get_db
from api.schemas.applications import ApplicationSchema, ApplicationUpdateStatusSchema
from api.services.applications import update_application
from api.services.users import verify_access_token
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix='/applications',  
    dependencies=[Depends(verify_access_token)], 
    tags=['Applications']
)


@router.patch('/{application_id}', response_model=ApplicationSchema)
async def patch_application(
    application_id: str, status: ApplicationUpdateStatusSchema, db: AsyncSession = Depends(get_db)
):
    updated_application = await update_application(db, application_id, status)
    
    return updated_application