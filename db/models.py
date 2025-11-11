import uuid
from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    String,
    DateTime,
    ForeignKey,
    Integer,
    Float,
    Boolean,
    JSON,
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import declarative_base, relationship
from pgvector.sqlalchemy import Vector

Base = declarative_base()

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_active = Column(DateTime, default=datetime.utcnow, nullable=False)
    meta_data = Column(JSON) # <-- RENAMED

    interactions = relationship("Interaction", back_populates="conversation")

class Interaction(Base):
    __tablename__ = "interactions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False, index=True)
    user_id = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    user_message = Column(String, nullable=False)
    assistant_message = Column(String, nullable=False)
    cognitive_plan = Column(JSON)
    memories_used = Column(ARRAY(UUID(as_uuid=True)))
    tokens_used = Column(Integer)
    cost = Column(Float)
    meta_data = Column(JSON) # <-- RENAMED

    conversation = relationship("Conversation", back_populates="interactions")
    episodic_memory = relationship("EpisodicMemory", back_populates="interaction", uselist=False)

class EpisodicMemory(Base):
    __tablename__ = "episodic_memories"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    interaction_id = Column(UUID(as_uuid=True), ForeignKey("interactions.id"), nullable=False)
    content = Column(String, nullable=False)
    embedding = Column(Vector(1536))
    timestamp = Column(DateTime, nullable=False, index=True)
    importance = Column(Float, nullable=False, default=0.5, index=True)
    attention_count = Column(Integer, nullable=False, default=0)
    last_accessed = Column(DateTime)
    meta_data = Column(JSON) # <-- RENAMED

    interaction = relationship("Interaction", back_populates="episodic_memory")

class CausalLink(Base):
    __tablename__ = "causal_links"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cause_memory_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    effect_memory_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    strength = Column(Float, nullable=False)
    type = Column(String(50), nullable=False)
    inferred_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    verified = Column(Boolean, default=False)