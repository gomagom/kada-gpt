from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Text,
)
from sqlalchemy.sql import func
from api.db import Base
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    email = Column(String(500))
    name = Column(String(1024), nullable=False, unique=True)
    password = Column(String(1024))
    is_admin = Column(Boolean, default=False)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    update_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    publish = Column(Boolean, default=True)

    group = relationship("Groups", back_populates="user")
    thread = relationship("Threads", back_populates="user")
    chat = relationship("Chat", back_populates="user")
    collection = relationship("Collections", back_populates="user")
    document = relationship("Documents", back_populates="user")


class Groups(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String(1024), nullable=False, unique=True)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    update_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    publish = Column(Boolean, default=True)
    user = relationship("Users", back_populates="group")
    thread = relationship("Threads", back_populates="group")
    collection = relationship("Collections", back_populates="group")


class Threads(Base):
    __tablename__ = "threads"

    id = Column(Integer, primary_key=True)
    create_user_id = Column(Integer, ForeignKey("users.id"))
    group_id = Column(Integer, ForeignKey("groups.id"))
    name = Column(String(1024))
    model_name = Column(String(100))
    search_method = Column(String(100))
    relate_num = Column(Integer)
    collections_id = Column(Integer, ForeignKey("collections.id"))
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    update_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    publish = Column(Boolean, default=True)
    user = relationship("Users", back_populates="thread")
    group = relationship("Groups", back_populates="thread")
    collection = relationship("Collections", back_populates="thread")
    chat = relationship("Chat", back_populates="thread")


class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True)
    create_user_id = Column(Integer, ForeignKey("users.id"))
    thread_id = Column(Integer, ForeignKey("threads.id"))
    collection_id = Column(Integer, ForeignKey("collections.id"))
    message_text = Column(Text)
    response_text = Column(Text)
    relate_num = Column(Integer)
    search_method = Column(String(100))
    model_name = Column(String(100))
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    update_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    references = Column(Text)
    publish = Column(Boolean, default=True)
    user = relationship("Users", back_populates="chat")
    thread = relationship("Threads", back_populates="chat")
    collection = relationship("Collections", back_populates="chat")


class Collections(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    create_user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(1024))
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    update_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    publish = Column(Boolean, default=True)
    user = relationship("Users", back_populates="collection")
    thread = relationship("Threads", back_populates="collection")
    group = relationship("Groups", back_populates="collection")
    document = relationship("Documents", back_populates="collection")
    chat = relationship("Chat", back_populates="collection")


class Documents(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    collection_id = Column(Integer, ForeignKey("collections.id"))
    create_user_id = Column(Integer, ForeignKey("users.id"))
    uri = Column(String(1000))
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    update_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    publish = Column(Boolean, default=True)
    user = relationship("Users", back_populates="document")
    collection = relationship("Collections", back_populates="document")
