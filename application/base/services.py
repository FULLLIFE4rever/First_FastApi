from sqlalchemy import delete, insert, select

from database import async_session


class BaseService:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session() as session:
            query = select(cls.model.__table__.columns).filter_by(id=model_id)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        query = select(cls.model.__table__.columns).filter_by(**filter_by)
        async with async_session() as session:
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_by_all(cls, **filter_by):
        query = select(cls.model.__table__.columns).filter_by(**filter_by)
        async with async_session() as session:
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def find_all(cls, *filters):
        query = select(cls.model.__table__.columns).filter(*filters)
        print(query)
        async with async_session() as session:
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(cls, **data):
        query = insert(cls.model).values(**data).returning(cls.model)
        async with async_session() as session:
            result = await session.execute(query)
            await session.commit()
        return result

    @classmethod
    async def delete(cls, **filter_by):
        async with async_session() as session:
            query = delete(cls.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()
