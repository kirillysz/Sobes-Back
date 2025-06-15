import json
import uuid

from typing import Optional
from datetime import datetime

from src.models.enums.role_enums import Role
from src.database.initialize import DatabaseInitializer

from src.models.enums.status_enums import Status
from src.utils.hashing import hash_value
from src.utils.data_time import dt_from_float

from pydantic import UUID4, Json

from src.config.database_config import QUERY_REGISTER_NEW_USER, QUERY_AUTH_USER, QUERY_GET_USER_BY_USERNAME, \
    QUERY_CREATE_TASK, QUERY_GET_TASK_BY_ID, QUERY_UPDATE_TASK_BY_ID, QUERY_DELETE_TASK_BY_ID, \
    QUERY_GET_TASK_FOR_ANALYTICS, QUERY_GET_ROLE_BY_ID, QUERY_GET_TASK_WITH_FILTER


class Database(DatabaseInitializer):
    def __init__(self, database_uri: str):
        super().__init__(database_uri=database_uri)

    async def get_user_by_username(self, username: str):
        await self.connect()

        result = await self.connection.fetch(
            QUERY_GET_USER_BY_USERNAME,
            username
        )

        return result

    async def get_role_by_id(self, user_id: UUID4):
        await self.connect()

        result = await self.connection.fetch(
            QUERY_GET_ROLE_BY_ID,
            user_id
        )

        return result


    async def register_new_user(self, username: str, role: Role, password: str) -> bool:
        await self.connect()

        id = uuid.uuid4()

        try:
            hashed_password = hash_value(password)
            if not await self.get_user_by_username(username):
                await self.connection.execute(
                    QUERY_REGISTER_NEW_USER,
                    id, username, role.value, hashed_password
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

            return result

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


    async def get_tasks_for_analytics(self,
                                     user_id: UUID4,
                                     status: str,
                                     from_date: float,
                                     to_date: float):
        await self.connect()

        try:
            result = await self.connection.fetch(
                QUERY_GET_TASK_FOR_ANALYTICS,
                user_id,
                status,
                from_date,
                to_date
            )

            return result

        except Exception as err:
            raise RuntimeError(err)

        finally:
            await self.close()


    async def create_task(self, id: UUID4,
                          user_id: UUID4,
                          title: str,
                          description: str,
                          status: Status,
                          created_at: float,
                          city: Optional[str] = None,
                          weather: Optional[dict] = None) -> bool:
        await self.connect()

        dt_created_at = dt_from_float(created_at)
        weather_json = json.dumps(weather) if weather is not None else None

        try:
            result = await self.connection.execute(
                QUERY_CREATE_TASK,
                id, user_id, title, description, status.value, dt_created_at, city, weather_json
            )

            if not result:
                return False

            return result

        except Exception as err:
            raise Exception(err)

        finally:
            await self.close()


    async def update_task_by_id(self,
                                task_id: UUID4,
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

    async def sort_tasks(self,
                         status: Optional[str] = None,
                         user: Optional[str] = None,
                         date: Optional[float] = None):

        await self.connect()

        filters = []
        values = []
        i = 1

        if status:
            filters.append(f"status = ${i}")
            values.append(status)
            i += 1

        if user:
            filters.append(f"user_id = ${i}")
            values.append(user)
            i += 1

        if date:
            filters.append(f"created_at >= ${i}")
            values.append(datetime.fromtimestamp(date))
            i += 1

        where_clause = " AND ".join(filters) if filters else "1=1"


        query = f"""
        SELECT * FROM tasks
        WHERE {where_clause}
        ORDER BY created_at DESC
        """

        try:
            result = await self.connection.fetch(query, *values)
            return result if result else None
        finally:
            await self.close()

async def main():
    db = Database(database_uri="postgresql://lazzy:admin@127.0.0.1:5432/test_back")

    # res = await db.get_tasks_for_analytics(
    #     user_id="046e70b2-5c84-4263-95db-12fb8276f6e8",
    #     status="todo",
    #     from_date="2025-05-24 21:22:11.870725",
    #     to_date="2025-05-24 21:22:11.870725"
    # )

    # print(res)
    # res = await db.register_new_user(
    #     username="1",
    #     role="admin",
    #     password="1"
    # )
    # print(res
    #       )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())