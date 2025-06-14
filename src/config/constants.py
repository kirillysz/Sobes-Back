from fastapi.security import OAuth2PasswordBearer
from src.settings import Settings
from src.database.crud import Database
from src.database.initialize import DatabaseInitializer

settings = Settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

db = Database(database_uri=settings.DATABASE_URI)
db_init = DatabaseInitializer(database_uri=settings.DATABASE_URI)