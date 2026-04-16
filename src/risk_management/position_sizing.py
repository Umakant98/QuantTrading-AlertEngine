Position sizing
from typing import Optional
from dataclasses import dataclass
import structlog

logger = structlog.get_logger(__name__)

@dataclass
class Position:
    symbol: str
    direction: str
    entry_price: float
    quantity: int
    stop_loss: float
    risk_amount: float
    position_size: float

class PositionSizer:
    def __init__(self, account_size: float, risk_per_trade_pct: float = 1.0):
        self.account_size = account_size
        self.risk_per_trade_pct = risk_per_trade_pct
        self.risk_per_trade = account_size * (risk_per_trade_pct / 100)
        logger.info("position_sizer_initialized", account_size=account_size)
    
    def calculate_position_size(self, entry_price: float, stop_loss: float, direction: str = "long") -> int:
        risk_per_unit = abs(entry_price - stop_loss)
        if risk_per_unit <= 0:
            return 0
        quantity = int(self.risk_per_trade / risk_per_unit)
        if quantity <= 0:
            return 0
        return quantity
    
    def calculate_risk_reward(self, entry_price: float, stop_loss: float, target_price: float) -> Optional[float]:
        risk = abs(entry_price - stop_loss)
        reward = abs(target_price - entry_price)
        if risk <= 0 or reward <= 0:
            return None
        return reward / risk
    
    def get_position(self, symbol: str, direction: str, entry_price: float, stop_loss: float, target_price: Optional[float] = None) -> Position:
        quantity = self.calculate_position_size(entry_price, stop_loss, direction)
        return Position(
            symbol=symbol,
            direction=direction,
            entry_price=entry_price,
            quantity=quantity,
            stop_loss=stop_loss,
            risk_amount=self.risk_per_trade,
            position_size=entry_price * quantity,
        )
