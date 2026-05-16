import asyncio
from sqlalchemy import text
from src.repository.database import async_db

async def fix_alembic():
    async with async_db.async_engine.begin() as conn:
        print("Checking alembic_version...")
        result = await conn.execute(text("SELECT version_num FROM alembic_version"))
        version = result.scalar()
        print(f"Current version in DB: {version}")
        
        # Force set to a known valid head from the files
        # We'll use pacing_practice_001
        print("Setting version to pacing_practice_001...")
        await conn.execute(text("UPDATE alembic_version SET version_num = 'pacing_practice_001'"))
        print("Done.")

if __name__ == "__main__":
    asyncio.run(fix_alembic())
