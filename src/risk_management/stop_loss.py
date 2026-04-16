Stop loss calculation
from typing import Optional
import structlog

logger = structlog.get_logger(__name__)

class StopLossCalculator:
    def __init__(self, atr_multiplier: float = 1.0):
        self.atr_multiplier = atr_multiplier
    
    def sl_from_structure(self, entry_price: float, swing_level: float, direction: str = "long", buffer_points: float = 0.1) -> float:
        if direction == "long":
            sl = swing_level - buffer_points
        else:
            sl = swing_level + buffer_points
        
        if direction == "long" and sl >= entry_price:
            sl = entry_price - 1
        elif direction == "short" and sl <= entry_price:
            sl = entry_price + 1
        
        return sl
    
    def sl_from_atr(self, entry_price: float, atr: float, direction: str = "long") -> float:
        sl_distance = atr * self.atr_multiplier
        if direction == "long":
            sl = entry_price - sl_distance
        else:
            sl = entry_price + sl_distance
        return sl
    
    def calculate_risk(self, entry_price: float, stop_loss: float, direction: str = "long") -> float:
        return abs(entry_price - stop_loss)
    
    def is_reasonable_sl(self, entry_price: float, stop_loss: float, max_risk_pct: float = 3.0) -> bool:
        risk = abs(entry_price - stop_loss)
        risk_pct = (risk / entry_price) * 100
        return risk_pct <= max_risk_pct
