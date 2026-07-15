import pytest
import pytest_asyncio
import asyncpg
from httpx import AsyncClient, ASGITransport
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.main import app
from app.core.database.session import Base, get_db
from app.core.limiter import limiter

TEST_DB_NAME = "fashop_test_db"
TEST_DATABASE_URL = f"postgresql+asyncpg://fashop_admin:fashop_secure_password@localhost:5432/{TEST_DB_NAME}"

# ─────────────────────────────────────────────────────────────
# Rate limiting — disabled per test, restored after each one.
# This prevents flaky 429s in business logic tests.
# Rate limiting is tested separately in test_rate_limit.py.
# ─────────────────────────────────────────────────────────────
@pytest.fixture(autouse=True)
def disable_rate_limit():
    limiter.enabled = False
    yield
    limiter.enabled = True


# ─────────────────────────────────────────────────────────────
# Session-scoped: runs ONCE per `pytest` invocation.
# Automatically creates the test database if it doesn't exist.
# Developers never need to run this manually.
# ─────────────────────────────────────────────────────────────
@pytest_asyncio.fixture(scope="session", autouse=True)
async def ensure_test_database():
    conn = await asyncpg.connect(
        host="localhost",
        port=5432,
        user="fashop_admin",
        password="fashop_secure_password",
        database="postgres"
    )
    db_exists = await conn.fetchval(
        "SELECT 1 FROM pg_database WHERE datname = $1", TEST_DB_NAME
    )
    if not db_exists:
        await conn.execute(f'CREATE DATABASE "{TEST_DB_NAME}"')
    await conn.close()


test_engine = create_async_engine(TEST_DATABASE_URL, echo=False, poolclass=pool.NullPool)
TestSessionLocal = async_sessionmaker(bind=test_engine, expire_on_commit=False)


# ─────────────────────────────────────────────────────────────
# Session-scoped: disposes the connection pool cleanly
# after the full test suite finishes. Prevents resource leaks.
# ─────────────────────────────────────────────────────────────
@pytest_asyncio.fixture(scope="session", autouse=True)
async def dispose_engine(ensure_test_database):
    yield
    await test_engine.dispose()


async def override_get_db():
    async with TestSessionLocal() as session:
        yield session


# ─────────────────────────────────────────────────────────────
# Function-scoped: runs before and after EACH test.
# Creates all tables → runs test → drops all tables.
# Clean isolated state for every test.
# ─────────────────────────────────────────────────────────────
@pytest_asyncio.fixture(autouse=True)
async def setup_database(ensure_test_database):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client():
    # setup_database is autouse=True so it runs automatically — no need to declare it here
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()