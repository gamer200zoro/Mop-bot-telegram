from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True) # Telegram user ID
    username = Column(String, unique=True, nullable=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, username=\'{self.username}\')>"

class Chat(Base):
    __tablename__ = "chats"

    id = Column(BigInteger, primary_key=True, index=True) # Telegram chat ID
    title = Column(String, nullable=True)
    type = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Chat(id={self.id}, title=\'{self.title}\')>"
