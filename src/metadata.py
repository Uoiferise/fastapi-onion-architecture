TAG_METADATA = [
    {
        "name": "v1",
        "description": "Operations with users v1",
    },
    {
        "name": "healthz",
        "description": "Standard service health check",
    },
]

TITLE = "FastAPI Onion Architecture"
DESCRIPTION = (
    "Implemented on FastAPI.\n\n"
    "Examples taken from the book - https://www.cosmicpython.com/book/chapter_06_uow.html.\n\n"
    "For contact - https://t.me/kalyukov_ns"
)
VERSION = "0.0.1"

ERRORS_MAP = {
    "mongo": "Mongo connection failed",
    "postgres": "PostgreSQL connection failed",
    "redis": "Redis connection failed",
    "rabbit": "RabbitMQ connection failed",
}
