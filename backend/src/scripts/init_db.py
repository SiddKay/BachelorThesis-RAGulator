import asyncio
from ..db import Base, db


async def init_db():
    try:
        await db.connect()
        async with db.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(init_db())
