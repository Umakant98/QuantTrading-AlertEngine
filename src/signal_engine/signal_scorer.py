Signal scoring
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from enum import Enum
import structlog

logger = structlog.get_logger(__name__)

class SignalGrade(str, Enum):
    A_PLUS = "A+"
    A = "A"
    B_PLUS = "B+"
    B = "B"
    C = "C"

@dataclass
class SignalFactor:
    name: str
    condition_met: bool
    weight: float
    value: float

@dataclass
class TradingSignal:
    timestamp: object
    symbol: str
    direction: str
    setup_type: str
    entry_zone: tuple
    stop_loss: float
    confidence_score: float
    grade: SignalGrade
    factors: List[SignalFactor] = field(default_factory=list)
    risk_reward_ratio: Optional[float] = None

class SignalScorer:
    def __init__(self, min_confidence: float = 70.0, min_factors: int = 3):
        self.min_confidence = min_confidence
        self.min_factors = min_factors
        self.weights = {
            "market_structure": 0.30,
            "order_flow": 0.25,
            "volatility": 0.20,
            "price_action": 0.15,
            "trend_alignment": 0.10,
        }
        logger.info("signal_scorer_initialized")
    
    def score_signal(self, factors: List[SignalFactor]) -> TradingSignal:
        if not factors:
            raise ValueError("No factors provided")
        
        score = 0.0
        weight_sum = 0.0
        
        for factor in factors:
            factor_weight = self.weights.get(factor.name, 0.1)
            weight_sum += factor_weight
            
            if factor.condition_met:
                score += factor.value * factor_weight
        
        confidence = (score / weight_sum * 100) if weight_sum > 0 else 0
        grade = self._assign_grade(confidence, len([f for f in factors if f.condition_met]))
        
        return TradingSignal(
            timestamp=None,
            symbol="",
            direction="",
            setup_type="",
            entry_zone=(0, 0),
            stop_loss=0,
            confidence_score=confidence,
            grade=grade,
            factors=factors,
        )
    
    def _assign_grade(self, confidence: float, factors_met: int) -> SignalGrade:
        if confidence >= 90 and factors_met >= 5:
            return SignalGrade.A_PLUS
        elif confidence >= 80 and factors_met >= 4:
            return SignalGrade.A
        elif confidence >= 70 and factors_met >= 3:
            return SignalGrade.B_PLUS
        elif confidence >= 60 and factors_met >= 3:
            return SignalGrade.B
        else:
            return SignalGrade.C
    
    def is_valid_signal(self, signal: TradingSignal) -> bool:
        met_factors = sum(1 for f in signal.factors if f.condition_met)
        return (signal.confidence_score >= self.min_confidence and met_factors >= self.min_factors)
    
    @staticmethod
    def build_factor(name: str, condition_met: bool, value: float = 1.0, weight: float = 1.0) -> SignalFactor:
        return SignalFactor(name=name, condition_met=condition_met, weight=weight, value=value)
