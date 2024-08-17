TAG_METADATA = [
    {
        'name': 'User | v1',
        'description': 'Operation with user v1.',
    },
    {
        'name': 'Company | v1',
        'description': 'Operation with company v1.',
    },
    {
        'name': 'healthz',
        'description': 'Standard health check.',
    },
]

TITLE = 'FastAPI Onion Architecture'
DESCRIPTION = (
    'Implemented on FastAPI.\n\n'
    'Examples taken from the book - https://www.cosmicpython.com/book/chapter_06_uow.html.\n\n'
    'For contact - https://t.me/kalyukov_ns'
)
VERSION = '0.0.1'

ERRORS_MAP = {
    'mongo': 'Mongo connection failed',
    'postgres': 'PostgreSQL connection failed',
    'redis': 'Redis connection failed',
    'rabbit': 'RabbitMQ connection failed',
}
