import asyncpg

from src.config.database_config import QUERY_CREATE_TABLES

class DatabaseInitializer:
    def __init__(self, database_uri: str):
        self.database = database_uri
        self.connection = None

    async def connect(self):
        try:
            self.connection = await asyncpg.connect(dsn=self.database)
        except Exception as err:
            raise Exception(err)

    async def close(self):
        try:
            await self.connection.close()
        except Exception as err:
            raise Exception(err)

    async def create_tables(self) -> bool:
        await self.connect()

        try:
            await self.connection.execute(
                QUERY_CREATE_TABLES
            )
            return True

        except asyncpg.DuplicateTableError as duplicate_error:
            pass

        except Exception as err:
            raise Exception(err)

        finally:
            await self.close()

