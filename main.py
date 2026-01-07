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


@app.get("/date")
async def get_date() -> Dict[str, str]:
    """Эндпоинт для получения текущей даты сервера"""
    now = datetime.now()
    return {
        "date": now.date().isoformat(),
        "formatted_date": now.strftime("%Y-%m-%d"),
        "day": now.strftime("%A"),
        "day_number": str(now.day),
        "month": now.strftime("%B"),
        "month_number": str(now.month),
        "year": str(now.year)
    }


@app.get("/datetime")
async def get_datetime() -> Dict[str, str]:
    """Эндпоинт для получения текущей даты и времени сервера"""
    now = datetime.now()
    return {
        "datetime": now.isoformat(),
        "date": now.date().isoformat(),
        "time": now.time().isoformat(),
        "timestamp": str(now.timestamp()),
        "formatted": now.strftime("%Y-%m-%d %H:%M:%S")
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

