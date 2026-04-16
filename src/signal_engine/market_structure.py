Market structure analysis
from typing import List, Optional, Dict
from dataclasses import dataclass
from datetime import datetime
import structlog
import numpy as np

logger = structlog.get_logger(__name__)

@dataclass
class StructureLevel:
    price: float
    timestamp: datetime
    bar_index: int
    type: str

@dataclass
class BreakOfStructure:
    direction: str
    broken_level: float
    break_price: float
    timestamp: datetime
    strength: float

class MarketStructureAnalyzer:
    def __init__(self, symbol: str, lookback_bos: int = 5, lookback_choc: int = 10):
        self.symbol = symbol
        self.lookback_bos = lookback_bos
        self.lookback_choc = lookback_choc
        self.bars = []
        self.structure_levels = []
        logger.info("structure_analyzer_created", symbol=symbol)
    
    def add_bar(self, bar_data: Dict) -> None:
        self.bars.append(bar_data)
        if len(self.bars) > 100:
            self.bars = self.bars[-100:]
        self._update_structure_levels()
    
    def _update_structure_levels(self) -> None:
        if len(self.bars) < 3:
            return
        idx = len(self.bars) - 2
        if idx < 1:
            return
        prev_bar = self.bars[idx - 1]
        curr_bar = self.bars[idx]
        next_bar = self.bars[idx + 1] if idx + 1 < len(self.bars) else None
        
        if curr_bar["high"] > prev_bar["high"]:
            if next_bar is None or curr_bar["high"] > next_bar["high"]:
                level = StructureLevel(
                    price=curr_bar["high"],
                    timestamp=curr_bar["timestamp"],
                    bar_index=idx,
                    type="high",
                )
                self._add_structure_level(level)
        
        if curr_bar["low"] < prev_bar["low"]:
            if next_bar is None or curr_bar["low"] < next_bar["low"]:
                level = StructureLevel(
                    price=curr_bar["low"],
                    timestamp=curr_bar["timestamp"],
                    bar_index=idx,
                    type="low",
                )
                self._add_structure_level(level)
    
    def _add_structure_level(self, level: StructureLevel) -> None:
        if self.structure_levels:
            last_level = self.structure_levels[-1]
            if abs(last_level.price - level.price) < 1:
                return
        self.structure_levels.append(level)
        if len(self.structure_levels) > 20:
            self.structure_levels = self.structure_levels[-20:]
    
    def detect_bos(self) -> Optional[BreakOfStructure]:
        if len(self.bars) < 2 or len(self.structure_levels) < 2:
            return None
        current_bar = self.bars[-1]
        current_price = current_bar["close"]
        recent_levels = self.structure_levels[-self.lookback_bos:]
        nearest_level = min(recent_levels, key=lambda x: abs(x.price - current_price))
        
        if nearest_level.type == "high" and current_price > nearest_level.price:
            strength = min(1.0, (current_price - nearest_level.price) / nearest_level.price)
            return BreakOfStructure(
                direction="bullish",
                broken_level=nearest_level.price,
                break_price=current_price,
                timestamp=current_bar["timestamp"],
                strength=strength,
            )
        elif nearest_level.type == "low" and current_price < nearest_level.price:
            strength = min(1.0, (nearest_level.price - current_price) / nearest_level.price)
            return BreakOfStructure(
                direction="bearish",
                broken_level=nearest_level.price,
                break_price=current_price,
                timestamp=current_bar["timestamp"],
                strength=strength,
            )
        return None
