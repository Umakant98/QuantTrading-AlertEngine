Helper utilities
from datetime import datetime
import pytz

IST = pytz.timezone('Asia/Kolkata')

def get_ist_now() -> datetime:
    return datetime.now(IST)

def is_market_open() -> bool:
    now = get_ist_now()
    if now.weekday() >= 5:
        return False
    market_open = now.replace(hour=9, minute=15, second=0)
    market_close = now.replace(hour=15, minute=30, second=0)
    return market_open <= now <= market_close

def is_high_liquidity_window() -> bool:
    now = get_ist_now()
    current_time = now.time()
    window_1_start = now.replace(hour=9, minute=15).time()
    window_1_end = now.replace(hour=11, minute=0).time()
    window_2_start = now.replace(hour=14, minute=30).time()
    window_2_end = now.replace(hour=15, minute=30).time()
    return (window_1_start <= current_time <= window_1_end or window_2_start <= current_time <= window_2_end)
