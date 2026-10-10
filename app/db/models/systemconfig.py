from typing import TYPE_CHECKING

from sqlalchemy import JSON, Column, String, select

from app.db import Base, async_db_query, db_query, db_update, get_id_column

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import Session


class SystemConfig(Base):
    """
    配置表
    """

    id = get_id_column()
    # 主键
    key = Column(String, index=True)
    # 值
    value = Column(JSON)

    @classmethod
    @db_query
    def get_by_key(cls, db: Session, key: str):
        return db.query(cls).filter(cls.key == key).first()

    @classmethod
    @async_db_query
    async def async_get_by_key(cls, db: AsyncSession, key: str):
        result = await db.execute(select(cls).where(cls.key == key))
        return result.scalar_one_or_none()

    @db_update
    def delete_by_key(self, db: Session, key: str):
        systemconfig = self.get_by_key(db, key)
        if systemconfig:
            systemconfig.delete(db, systemconfig.id)
        return True
