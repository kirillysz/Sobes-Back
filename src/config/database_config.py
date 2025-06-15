QUERY_CREATE_TABLES = """
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_role') THEN
        CREATE TYPE user_role AS ENUM ('admin', 'user');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'task_status') THEN
        CREATE TYPE task_status AS ENUM ('todo', 'in_progress', 'done');
    END IF;
END$$;

CREATE TABLE IF NOT EXISTS users(
    id UUID UNIQUE,
    username TEXT NOT NULL UNIQUE,
    role user_role,
    password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tasks(
    id UUID UNIQUE,
    user_id UUID NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    status task_status,
    created_at TIMESTAMP,
    city TEXT,
    weather jsonb,
    
    FOREIGN KEY (user_id) REFERENCES users (id)
)
"""

QUERY_REGISTER_NEW_USER = """INSERT INTO users(id, username, role, password_hash) VALUES($1, $2, $3, $4)"""
QUERY_AUTH_USER = "SELECT * FROM users WHERE username = $1 AND password_hash = $2"
QUERY_GET_USER_BY_USERNAME = "SELECT id FROM users WHERE username = $1"
QUERY_GET_ROLE_BY_ID = "SELECT role FROM users WHERE id = $1"


QUERY_GET_TASK_BY_ID = "SELECT user_id, title, description, status, created_at, city, weather FROM tasks WHERE id = $1"
QUERY_GET_TASK_FOR_ANALYTICS = "SELECT id, title, description, created_at, city, weather FROM tasks WHERE user_id = $1 AND status = $2 AND created_at BETWEEN $3 AND $4"
QUERY_CREATE_TASK = """
    INSERT INTO tasks(id, user_id, title, description, status, created_at, city, weather) 
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
"""
QUERY_DELETE_TASK_BY_ID = "DELETE FROM tasks WHERE id = $1"
QUERY_UPDATE_TASK_BY_ID = "UPDATE tasks SET"
QUERY_GET_TASK_WITH_FILTER = "SELECT * FROM tasks WHERE"