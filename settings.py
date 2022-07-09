import os

from dotenv import load_dotenv

load_dotenv()
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
ALGORITHMS = os.environ.get("ALGORITHMS")
API_AUDIENCE = os.environ.get("API_AUDIENCE")
CASTING_ASSISTANT_JWT = os.environ.get("CASTING_ASSISTANT_TOKEN")
CASTING_DIRECTOR_JWT = os.environ.get("CASTING_DIRECTOR_TOKEN")
EXECUTIVE_PRODUCER_JWT = os.environ.get("EXECUTIVE_PRODUCER_TOKEN")