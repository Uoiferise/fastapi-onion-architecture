"""Contains helper functions for tests."""

from collections.abc import Iterable, Sequence
from typing import Any

from pydantic import BaseModel
from requests import Response
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase


async def bulk_save_models(
    session: AsyncSession,
    model: type[DeclarativeBase],
    data: Iterable[dict[str, Any]],
    *,
    commit: bool = False,
) -> None:
    """Bulk saves model objects to the database."""
    for values in data:
        await session.execute(insert(model).values(**values))

    if commit:
        await session.commit()
    else:
        await session.flush()


def compare_dicts_and_db_models(
    result: Sequence[DeclarativeBase] | None,
    expected_result: Sequence[dict] | None,
    schema: type[BaseModel],
) -> bool:
    """Compares models from the database with expected dictionaries.
    Bring everything to the same Pydantic schema.
    """
    if result is None or expected_result is None:
        return result == expected_result

    result_to_schema = [schema(**item.__dict__) for item in result]
    expected_result_to_schema = [schema(**item) for item in expected_result]

    equality_len = len(result_to_schema) == len(expected_result_to_schema)
    equality_obj = all(obj in expected_result_to_schema for obj in result_to_schema)
    return all((equality_len, equality_obj))


def prepare_payload(response: Response, exclude: Sequence[str] | None = None) -> dict:
    """Extracts the payload from the response."""
    payload = response.json().get('payload')
    if payload is None:
        return {}

    if exclude is None:
        return payload

    for key in exclude:
        payload.pop(key, None)

    return payload
