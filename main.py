from fastapi import FastAPI, HTTPException, Query
from datetime import datetime
from typing import Dict, Optional
from zoneinfo import ZoneInfo

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


# Маппинг популярных городов на часовые пояса
TIMEZONE_MAP = {
    "екатеринбург": "Asia/Yekaterinburg",
    "ekaterinburg": "Asia/Yekaterinburg",
    "москва": "Europe/Moscow",
    "moscow": "Europe/Moscow",
    "санкт-петербург": "Europe/Moscow",
    "saint-petersburg": "Europe/Moscow",
    "st-petersburg": "Europe/Moscow",
    "новосибирск": "Asia/Novosibirsk",
    "novosibirsk": "Asia/Novosibirsk",
    "красноярск": "Asia/Krasnoyarsk",
    "krasnoyarsk": "Asia/Krasnoyarsk",
    "иркутск": "Asia/Irkutsk",
    "irkutsk": "Asia/Irkutsk",
    "владивосток": "Asia/Vladivostok",
    "vladivostok": "Asia/Vladivostok",
    "лондон": "Europe/London",
    "london": "Europe/London",
    "нью-йорк": "America/New_York",
    "new-york": "America/New_York",
    "newyork": "America/New_York",
    "токио": "Asia/Tokyo",
    "tokyo": "Asia/Tokyo",
    "пекин": "Asia/Shanghai",
    "beijing": "Asia/Shanghai",
    "шанхай": "Asia/Shanghai",
    "shanghai": "Asia/Shanghai",
}


def normalize_timezone(timezone: str) -> str:
    """Нормализует название часового пояса"""
    timezone_lower = timezone.lower().strip()
    
    # Проверяем маппинг городов
    if timezone_lower in TIMEZONE_MAP:
        return TIMEZONE_MAP[timezone_lower]
    
    # Если уже в формате IANA (например, Asia/Yekaterinburg), возвращаем как есть
    return timezone


@app.get("/convert-time")
async def convert_time(
    time: str = Query(..., description="Время в формате 'HH:MM' или 'YYYY-MM-DD HH:MM:SS' (в UTC)"),
    timezone: str = Query(..., description="Часовой пояс (например, 'Asia/Yekaterinburg' или 'Екатеринбург')")
) -> Dict[str, str]:
    """
    Конвертирует время из UTC в указанный часовой пояс.
    
    Примеры:
    - time=15:00&timezone=Екатеринбург -> 20:00 (UTC+5)
    - time=2024-01-15 15:00:00&timezone=Asia/Yekaterinburg -> 2024-01-15 20:00:00
    """
    try:
        # Нормализуем часовой пояс
        tz_name = normalize_timezone(timezone)
        
        # Парсим входное время
        time_str = time.strip()
        
        # Пробуем разные форматы
        dt_utc = None
        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%H:%M:%S",
            "%H:%M",
        ]
        
        for fmt in formats:
            try:
                dt_utc = datetime.strptime(time_str, fmt)
                break
            except ValueError:
                continue
        
        if dt_utc is None:
            raise ValueError(f"Не удалось распарсить время: {time_str}")
        
        # Если указано только время без даты, используем сегодняшнюю дату
        if len(time_str) <= 8:  # Только время (HH:MM или HH:MM:SS)
            today = datetime.now().date()
            dt_utc = datetime.combine(today, dt_utc.time())
        
        # Устанавливаем, что время в UTC
        dt_utc = dt_utc.replace(tzinfo=ZoneInfo("UTC"))
        
        # Конвертируем в указанный часовой пояс
        try:
            target_tz = ZoneInfo(tz_name)
        except Exception as e:
            raise ValueError(f"Неверный часовой пояс: {timezone}. Ошибка: {str(e)}")
        
        dt_target = dt_utc.astimezone(target_tz)
        
        return {
            "input_time_utc": dt_utc.strftime("%Y-%m-%d %H:%M:%S %Z"),
            "converted_time": dt_target.strftime("%Y-%m-%d %H:%M:%S"),
            "converted_time_iso": dt_target.isoformat(),
            "time_only": dt_target.strftime("%H:%M:%S"),
            "timezone": tz_name,
            "utc_offset": dt_target.strftime("%z"),
            "utc_offset_hours": str(int(dt_target.utcoffset().total_seconds() / 3600))
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при конвертации времени: {str(e)}")


@app.get("/timezones")
async def get_timezones() -> Dict[str, Dict[str, str]]:
    """
    Возвращает список популярных часовых поясов с их IANA названиями.
    Можно использовать как название города, так и IANA формат.
    """
    return {
        "popular_timezones": TIMEZONE_MAP,
        "note": "Вы можете использовать как название города (например, 'Екатеринбург'), так и IANA формат (например, 'Asia/Yekaterinburg')"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

