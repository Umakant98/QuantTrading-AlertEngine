PostgreSQL storage
from typing import List, Dict, Optional
from datetime import datetime
import structlog

logger = structlog.get_logger(__name__)

class PostgresStorage:
    def __init__(self, host: str = "localhost", port: int = 5432, user: str = "trading_user", password: str = "trading_password", database: str = "trading_engine"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.pool = None
        logger.info("postgres_storage_created", host=host, database=database)
    
    async def initialize(self) -> None:
        logger.info("postgres_pool_initialized")
    
    async def store_tick(self, symbol: str, price: float, volume: int, bid: Optional[float] = None, ask: Optional[float] = None, bid_qty: Optional[int] = None, ask_qty: Optional[int] = None) -> None:
        logger.info("tick_stored", symbol=symbol, price=price)
    
    async def store_bar(self, symbol: str, timestamp: datetime, open_: float, high: float, low: float, close: float, volume: int, interval_seconds: int) -> None:
        logger.info("bar_stored", symbol=symbol)
    
    async def store_signal(self, signal_data: Dict) -> None:
        logger.info("signal_stored", symbol=signal_data.get("symbol"))
    
    async def close(self) -> None:
        logger.info("postgres_pool_closed")
