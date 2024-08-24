from collections.abc import Awaitable, Callable
from datetime import datetime
from typing import Annotated, Any
from uuid import uuid4

from sqlalchemy import UUID, DateTime, Integer, text
from sqlalchemy.orm import mapped_column

AsyncFunc = Callable[..., Awaitable[Any]]

integer_pk = Annotated[int, mapped_column(Integer, primary_key=True)]
uuid_pk = Annotated[uuid4, mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)]

dt_now_utc_sql = text("TIMEZONE('utc', now())")
created_at = Annotated[datetime, mapped_column(DateTime, server_default=dt_now_utc_sql)]
updated_at = Annotated[datetime, mapped_column(
    DateTime,
    server_default=dt_now_utc_sql,
    onupdate=dt_now_utc_sql,
)]
