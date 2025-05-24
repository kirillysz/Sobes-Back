import uuid
import asyncpg

from typing import Optional
from src.database.initialize import DatabaseInitializer
from src.uitls.hashing import hash_value

from pydantic import UUID4, Json

from src.config.database_config import QUERY_REGISTER_NEW_USER, QUERY_AUTH_USER, QUERY_GET_USER_BY_USERNAME, \
    QUERY_CREATE_TASK, QUERY_GET_TASK_BY_ID, QUERY_UPDATE_TASK_BY_ID, QUERY_DELETE_TASK_BY_ID


class Database(DatabaseInitializer):
    def __init__(self, database_uri: str):
        super().__init__(database_uri=database_uri)

    async def get_user_by_username(self, username: str):
        result = await self.connection.fetch(
            QUERY_GET_USER_BY_USERNAME,
            username
        )

        return result

    async def register_new_user(self, username: str, role: str, password: str) -> bool:
        await self.connect()

        id = uuid.uuid4()

        try:
            hashed_password = hash_value(password)
            if not await self.get_user_by_username(username):
                await self.connection.execute(
                    QUERY_REGISTER_NEW_USER,
                    id, username, role, hashed_password
                )
                return True
            else:
                return False

        except Exception as err:
            raise Exception(err)

        finally:
            await self.close()

    async def auth_user(self, username: str, password: str) -> bool:
        await self.connect()

        try:
            hashed_password = hash_value(password)
            result = await self.connection.fetch(
                QUERY_AUTH_USER,
                username, hashed_password
            )

            if not result:
                return False

            return True

        except Exception as err:
            raise Exception(err)

        finally:
            await self.close()


    async def get_task_by_id(self, task_id: UUID4):
        await self.connect()

        try:
            result = await self.connection.fetch(
                QUERY_GET_TASK_BY_ID,
                task_id
            )
            return result

        except Exception as err:
            raise Exception(err)

    async def create_task(self, id: UUID4,
                          user_id: UUID4,
                          title: str,
                          description: str,
                          status: str,
                          created_at: float,
                          city: Optional[str] = None,
                          weather: Optional[Json] = None) -> bool:
        await self.connect()

        try:
            result = await self.connection.execute(
                QUERY_CREATE_TASK,
                id, user_id, title, description, status, created_at, city, weather
            )

            if not result:
                return False

            return True

        except asyncpg.DuplicateSchemaError as duplicate_err:
            pass

        except Exception as err:
            raise Exception(err)

        finally:
            await self.close()

    async def update_task_by_id(self, task_id: UUID4,
                                title: Optional[str] = None,
                                description: Optional[str] = None,
                                status: Optional[str] = None,
                                created_at: Optional[float] = None,
                                city: Optional[str] = None,
                                weather: Optional[Json] = None
                                ):
        await self.connect()

        fields = {
            "title": title,
            "description": description,
            "status": status,
            "created_at": created_at,
            "city": city,
            "weather": weather,
        }

        updates = {k: v for k, v in fields.items() if v is not None}

        if not updates:
            return

        set_parts = []
        values = []
        i = 1

        for column, value in updates.items():
            set_parts.append(f"{column} = ${i}")
            values.append(value)
            i += 1

        values.append(task_id)
        set_clause = ", ".join(set_parts)

        query = f"{QUERY_UPDATE_TASK_BY_ID} {set_clause} WHERE id = ${i}"

        try:
            await self.connection.execute(
                query, *values
            )
            return True

        except Exception as err:
            raise Exception(err)

    async def delete_task_by_id(self, task_id: UUID4):
        await self.connect()

        try:
            await self.connection.execute(
                QUERY_DELETE_TASK_BY_ID,
                task_id
            )
            return True

        except Exception as err:
            raise Exception(err)

async def main():
    db = Database(database_uri="postgresql://lazzy:admin@127.0.0.1:5432/test_back")

    res = await db.update_task_by_id(
        task_id="87aaedfb-60aa-4238-bd9f-f0c743b99177",
        title="NEW TITLE"
    )
    print(res)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())