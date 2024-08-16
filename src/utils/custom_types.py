from collections.abc import Awaitable, Callable
from datetime import datetime
from typing import Annotated, Any
from uuid import uuid4

from sqlalchemy import UUID, DateTime, Integer, String, text
from sqlalchemy.orm import mapped_column

async_func = Callable[..., Awaitable[Any]]

dt_now_utc = text("TIMEZONE('utc', now())")

integer_pk = Annotated[int, mapped_column(Integer, primary_key=True)]
uuid_pk = Annotated[uuid4, mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)]

created_at = Annotated[datetime, mapped_column(DateTime, server_default=dt_now_utc)]
updated_at = Annotated[datetime, mapped_column(
    DateTime,
    server_default=dt_now_utc,
    onupdate=dt_now_utc,
)]

string_50 = Annotated[str, mapped_column(String(50))]
string_50_nullable = Annotated[str | None, mapped_column(String(50), nullable=True, default=None)]
