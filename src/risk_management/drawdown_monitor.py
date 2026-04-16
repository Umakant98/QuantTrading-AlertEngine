Drawdown monitoring
from datetime import datetime, date
from typing import Dict, Optional
import structlog

logger = structlog.get_logger(__name__)

class DrawdownMonitor:
    def __init__(self, starting_capital: float, max_daily_loss_pct: float = 5.0, max_trades_per_day: int = 10):
        self.starting_capital = starting_capital
        self.max_daily_loss_pct = max_daily_loss_pct
        self.max_trades_per_day = max_trades_per_day
        self.current_date = None
        self.daily_pnl = 0.0
        self.daily_trades = 0
        self.daily_history = {}
        logger.info("drawdown_monitor_initialized", capital=starting_capital)
    
    def record_trade(self, pnl: float) -> None:
        today = date.today()
        if self.current_date != today:
            self._reset_day(today)
        self.daily_pnl += pnl
        self.daily_trades += 1
    
    def _reset_day(self, new_date: date) -> None:
        if self.current_date is not None:
            self.daily_history[self.current_date] = {
                "pnl": self.daily_pnl,
                "trades": self.daily_trades,
            }
        self.current_date = new_date
        self.daily_pnl = 0.0
        self.daily_trades = 0
    
    def can_trade(self) -> bool:
        max_daily_loss = self.starting_capital * (self.max_daily_loss_pct / 100)
        if self.daily_pnl < -max_daily_loss:
            return False
        if self.daily_trades >= self.max_trades_per_day:
            return False
        return True
    
    def get_daily_stats(self) -> Dict:
        return {
            "date": self.current_date,
            "pnl": self.daily_pnl,
            "trades": self.daily_trades,
            "can_trade": self.can_trade(),
        }
