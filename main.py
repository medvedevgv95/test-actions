from fastapi import FastAPI
from datetime import datetime
from typing import Dict

app = FastAPI(title="Time Server API", version="1.0.0")


@app.get("/")
async def root() -> Dict[str, str]:
    """Возвращает текущее время сервера"""
    return {
        "current_time": datetime.now().isoformat(),
        "message": "Server time retrieved successfully"
    }


@app.get("/time")
async def get_time() -> Dict[str, str]:
    """Эндпоинт для получения текущего времени сервера"""
    return {
        "server_time": datetime.now().isoformat(),
        "timestamp": str(datetime.now().timestamp())
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

