Spread monitoring
from typing import Optional
import structlog

logger = structlog.get_logger(__name__)

class SpreadMonitor:
    def __init__(self, max_spread_bps: int = 5):
        self.max_spread_bps = max_spread_bps
        self.spread_history = []
    
    def record_spread(self, spread_bps: float) -> None:
        self.spread_history.append(spread_bps)
        if len(self.spread_history) > 100:
            self.spread_history = self.spread_history[-100:]
    
    def is_spread_acceptable(self, current_spread_bps: float) -> bool:
        return current_spread_bps <= self.max_spread_bps
    
    def get_avg_spread(self) -> Optional[float]:
        if not self.spread_history:
            return None
        return sum(self.spread_history) / len(self.spread_history)
