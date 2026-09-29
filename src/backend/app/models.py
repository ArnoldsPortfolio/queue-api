from datetime import datetime
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base
from app.kernel.ids import new_id
class UserRow(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    email: Mapped[str] = mapped_column(String(320), unique=True)
    password_hash: Mapped[str] = mapped_column(String(128))
class ApiKeyRow(Base):
    __tablename__ = "api_keys"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    owner_id: Mapped[str] = mapped_column(String(36), index=True)
    name: Mapped[str] = mapped_column(String(80))
    prefix: Mapped[str] = mapped_column(String(12), index=True)
    secret_hash: Mapped[str] = mapped_column(String(128))
    revoked: Mapped[int] = mapped_column(Integer, default=0)
class JobRow(Base):
    __tablename__ = "jobs"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    owner_id: Mapped[str] = mapped_column(String(36), index=True)
    kind: Mapped[str] = mapped_column(String(40))
    payload: Mapped[str] = mapped_column(Text, default="{}")
    status: Mapped[str] = mapped_column(String(20), default="queued")
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    result: Mapped[str] = mapped_column(Text, default="")
    error: Mapped[str] = mapped_column(Text, default="")
    idempotency_key: Mapped[str] = mapped_column(String(80), default="")
    run_after: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
class WebhookRow(Base):
    __tablename__ = "webhooks"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    owner_id: Mapped[str] = mapped_column(String(36), index=True)
    url: Mapped[str] = mapped_column(String(300))
    secret: Mapped[str] = mapped_column(String(80))
class RateRow(Base):
    __tablename__ = "rate_hits"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    key_id: Mapped[str] = mapped_column(String(36), index=True)
    at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
