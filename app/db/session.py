from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = (
    "postgresql+asyncpg://postgres:postgres@db:5432/postgres"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
)

