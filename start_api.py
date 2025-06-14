from src.app.api.v1.app import app

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        app=app
    )