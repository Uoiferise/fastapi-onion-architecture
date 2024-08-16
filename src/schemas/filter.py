from dataclasses import dataclass

from fastapi import Query


@dataclass
class BaseFilter:
    page: int | None = Query(default=None)
    per_page: int = Query(ge=1, le=100, default=100)

    @property
    def offset(self) -> int:
        return self.page * self.per_page if self.page else 0

    @property
    def limit(self) -> int | None:
        return self.per_page if self.page is not None else None


@dataclass
class TypeFilter(BaseFilter):
    like: str = Query(default='')
