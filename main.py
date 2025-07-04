from fastapi import FastAPI

from api.routers.candidates import router as candidates_router
from api.routers.applications import router as applications_router
from api.routers.users import router as users_router


app = FastAPI(
    title="Candidate Management API",
    description="API to manage job applications and candidates",
    version="1.0.0",
    openapi_tags=[
        {"name": "Candidates", "description": "Operations with candidates"},
        {"name": "Applications", "description": "Manage job applications"},
    ]
)

app.include_router(candidates_router)
app.include_router(applications_router)
app.include_router(users_router)

@app.get('/')
async def index():
    return 'Welcome to Candidate Management API'
