Slippage simulation
from typing import Optional
import random
import structlog

logger = structlog.get_logger(__name__)

class SlippageSimulator:
    def __init__(self, base_slippage_bps: int = 2, vol_sensitive: bool = True):
        self.base_slippage_bps = base_slippage_bps
        self.vol_sensitive = vol_sensitive
    
    def calculate_slippage(self, price: float, quantity: int, spread_bps: int, volatility_regime: str = "neutral") -> float:
        slippage_bps = self.base_slippage_bps + spread_bps
        if self.vol_sensitive:
            if volatility_regime == "expansion":
                slippage_bps *= 1.5
            elif volatility_regime == "contraction":
                slippage_bps *= 0.7
        slippage_rupees = (price * quantity * slippage_bps) / 10000
        return slippage_rupees
    
    def apply_slippage(self, entry_price: float, direction: str = "long") -> float:
        slippage_fraction = self.base_slippage_bps / 10000
        slippage_amount = entry_price * slippage_fraction
        if direction == "long":
            return entry_price + slippage_amount
        else:
            return entry_price - slippage_amount
