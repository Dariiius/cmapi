import asyncio
from sqlalchemy import select
from passlib.context import CryptContext
from api.core.db import SessionLocal
from api.models.users import Users

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

async def seed():
    async with SessionLocal() as db:
        result = await db.execute(select(Users).where(Users.email == 'admin@example.com'))
        admin = result.scalar_one_or_none()

        if not admin:
            user = Users(
                email='admin@example.com',
                password=pwd_context.hash('admin')
            )
            db.add(user)
            await db.commit()
            print('Admin user created.')
        else:
            print('Admin user already exists.')


if __name__ == '__main__':
    asyncio.run(seed())