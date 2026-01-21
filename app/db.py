from collections. abc import AsyncGenerator
import uuid
import datetime

from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship

# allows to connect to loal db file
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# for any database need to define the structure of the data
# create a data model for storing a Post

class Post(DeclarativeBase):
    __tablename__ = "posts"

    # id needed for every single entity, since it's a primary key
    # the following line generates a new unique id
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # structure of these variables, caption is a name, Column as opposed to relationship, string for data type in sql

    caption = Column(Text)
    url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

# 1.starts engine, 2. creates the db
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(DeclarativeBase.metadata.create_all)

# creates the session, WHICH allows to write, read asynchronously
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
