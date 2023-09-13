from src.database.database import engine
from src.models.users import Base


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    import asyncio

    print(engine)
    asyncio.run(init_models())
