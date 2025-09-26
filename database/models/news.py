from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    func,
)
import uuid
from sqlalchemy.dialects.postgresql import JSONB, UUID
from database.setup import Base

class News(Base):
    __tablename__ = "news"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid(), default=uuid.uuid4)

    
    created_at = Column(DateTime, server_default=func.now(), comment="Timestamp da criação do registro no banco.")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="Timestamp da última atualização do registro.")


