Backtest metrics
from typing import List, Dict
import numpy as np
import structlog

logger = structlog.get_logger(__name__)

class BacktestMetrics:
    @staticmethod
    def calculate_metrics(trades: List[Dict], initial_capital: float, risk_free_rate: float = 0.06) -> Dict:
        if not trades:
            return {}
        return {
            "total_trades": len(trades),
            "win_rate": 0,
            "profit_factor": 0,
            "sharpe_ratio": 0,
            "max_drawdown_pct": 0,
        }
