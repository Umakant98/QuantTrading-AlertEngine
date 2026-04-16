Order flow analysis
from typing import List, Optional, Dict
from dataclasses import dataclass
import numpy as np
import structlog

logger = structlog.get_logger(__name__)

@dataclass
class VolumeDelta:
    total_volume: int
    up_volume: int
    down_volume: int
    delta: int
    delta_ratio: float

class OrderFlowAnalyzer:
    def __init__(self, symbol: str, lookback_volume: int = 20):
        self.symbol = symbol
        self.lookback_volume = lookback_volume
        self.bars = []
    
    def add_bar(self, bar_data: Dict) -> None:
        self.bars.append(bar_data)
        if len(self.bars) > 100:
            self.bars = self.bars[-100:]
    
    def calculate_volume_delta(self, lookback: int = 20) -> Optional[VolumeDelta]:
        if len(self.bars) < 2:
            return None
        
        bars_to_analyze = self.bars[-lookback:]
        up_volume = 0
        down_volume = 0
        total_volume = 0
        
        for i, bar in enumerate(bars_to_analyze):
            if i == 0:
                continue
            volume = bar.get("volume", 0)
            total_volume += volume
            if bar["close"] >= bar["open"]:
                up_volume += volume
            else:
                down_volume += volume
        
        delta = up_volume - down_volume
        delta_ratio = up_volume / down_volume if down_volume > 0 else 0
        
        return VolumeDelta(
            total_volume=total_volume,
            up_volume=up_volume,
            down_volume=down_volume,
            delta=delta,
            delta_ratio=delta_ratio,
        )
    
    def detect_liquidity_spike(self, threshold_multiplier: float = 2.0) -> bool:
        if len(self.bars) < self.lookback_volume + 1:
            return False
        
        current_bar = self.bars[-1]
        current_volume = current_bar.get("volume", 0)
        
        recent_bars = self.bars[-(self.lookback_volume + 1):-1]
        avg_volume = np.mean([b.get("volume", 0) for b in recent_bars])
        
        spike = current_volume > avg_volume * threshold_multiplier
        
        if spike:
            logger.info("liquidity_spike_detected", symbol=self.symbol)
        
        return spike
    
    def analyze_candle_imbalance(self, threshold: float = 0.7) -> Optional[Dict]:
        if len(self.bars) < 1:
            return None
        
        bar = self.bars[-1]
        body = abs(bar["close"] - bar["open"])
        total_range = bar["high"] - bar["low"]
        
        if total_range == 0:
            return None
        
        body_ratio = body / total_range
        imbalance_detected = body_ratio > threshold
        
        return {
            "body_ratio": body_ratio,
            "imbalanced": imbalance_detected,
            "direction": "bullish" if bar["close"] > bar["open"] else "bearish",
            "strength": min(1.0, body_ratio),
        }
