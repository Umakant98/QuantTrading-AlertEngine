Volatility regime analysis
from typing import List, Optional, Dict
from dataclasses import dataclass
import numpy as np
import structlog

logger = structlog.get_logger(__name__)

@dataclass
class VolatilityRegime:
    current_atr: float
    historical_avg_atr: float
    regime: str
    expansion_factor: float

class VolatilityAnalyzer:
    def __init__(self, symbol: str, atr_period: int = 14):
        self.symbol = symbol
        self.atr_period = atr_period
        self.bars = []
        self.atr_values = []
    
    def add_bar(self, bar_data: Dict) -> None:
        self.bars.append(bar_data)
        if len(self.bars) > 200:
            self.bars = self.bars[-200:]
        
        atr = self._calculate_atr()
        self.atr_values.append(atr)
        
        if len(self.atr_values) > 100:
            self.atr_values = self.atr_values[-100:]
    
    def _calculate_atr(self) -> float:
        if len(self.bars) < self.atr_period:
            return 0.0
        
        recent_bars = self.bars[-self.atr_period:]
        true_ranges = []
        
        for i, bar in enumerate(recent_bars):
            if i == 0:
                tr = bar["high"] - bar["low"]
            else:
                prev_close = recent_bars[i - 1]["close"]
                tr = max(
                    bar["high"] - bar["low"],
                    abs(bar["high"] - prev_close),
                    abs(bar["low"] - prev_close),
                )
            true_ranges.append(tr)
        
        return np.mean(true_ranges)
    
    def get_volatility_regime(self, expansion_threshold: float = 1.3, contraction_threshold: float = 0.7) -> VolatilityRegime:
        if not self.atr_values:
            return VolatilityRegime(0, 0, "neutral", 1.0)
        
        current_atr = self.atr_values[-1]
        historical_avg = np.mean(self.atr_values)
        
        if historical_avg == 0:
            return VolatilityRegime(current_atr, 0, "neutral", 1.0)
        
        expansion_factor = current_atr / historical_avg
        
        if expansion_factor > expansion_threshold:
            regime = "expansion"
        elif expansion_factor < contraction_threshold:
            regime = "contraction"
        else:
            regime = "neutral"
        
        return VolatilityRegime(
            current_atr=current_atr,
            historical_avg_atr=historical_avg,
            regime=regime,
            expansion_factor=expansion_factor,
        )
    
    def get_current_atr(self) -> float:
        return self.atr_values[-1] if self.atr_values else 0.0
