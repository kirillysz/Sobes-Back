from datetime import datetime

def human_to_timestamp(human_date: str) -> datetime:
    "Принимает Human_date в формате: 2025-05-24 21:22:11.870725. после точки - мс"
    return datetime.strptime(human_date, "%Y-%m-%d %H:%M:%S.%f")