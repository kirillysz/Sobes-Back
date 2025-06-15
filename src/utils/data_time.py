from datetime import datetime

def dt_from_float(float_date: float):
    return datetime.fromtimestamp(float_date)