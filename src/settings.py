from pydantic_settings import BaseSettings  # не просто BaseModel

class Settings(BaseSettings):
      SECRET: str
      DATABASE_URI: str
      ACCESS_TOKEN_EXPIRE_MINUTES: int

      class Config:
         env_file = "src/.env"
         env_file_encoding = "utf-8"
         