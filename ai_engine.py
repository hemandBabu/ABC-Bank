import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression

class UnifiedFinancialAI:
    def __init__(self):
        self.fraud_detector = IsolationForest(contamination=0.05, random_state=42)
        self.cashflow_model = LinearRegression()
        
    def train_behavioral_profile(self, history_df):
        if len(history_df) > 0:
            features = history_df[['amount', 'hour_of_day', 'day_of_week']]
            self.fraud_detector.fit(features)
        
    def evaluate_transaction(self, transaction):
        features = np.array([[transaction['amount'], transaction['hour_of_day'], transaction['day_of_week']]])
        raw_score = self.fraud_detector.decision_function(features)[0]
        is_anomaly = self.fraud_detector.predict(features)[0] == -1
        risk_score = float(np.clip((1 - (raw_score + 0.5)) * 100, 0, 100))
        return {
            "is_high_risk": bool(is_anomaly),
            "risk_score": round(risk_score, 2),
            "flag_reason": "Unusual spending pattern detected" if is_anomaly else "Normal"
        }

    def forecast_cash_flow(self, daily_balances):
        X = np.arange(len(daily_balances)).reshape(-1, 1)
        y = np.array(daily_balances)
        self.cashflow_model.fit(X, y)
        
        future_X = np.arange(len(daily_balances), len(daily_balances) + 30).reshape(-1, 1)
        forecast = self.cashflow_model.predict(future_X)
        shortages = [int(day) for day, balance in enumerate(forecast) if balance < 0]
        
        return {
            "forecasted_balances": [round(b, 2) for b in forecast.tolist()],
            "potential_shortage_days": shortages,
            "liquidity_status": "Critical: Shortages Expected" if shortages else "Healthy"
        }

    def calculate_goal(self, current_savings, target_amount, target_months, avg_monthly_surplus):
        remaining = target_amount - current_savings
        required_monthly = remaining / max(target_months, 1)
        is_achievable = avg_monthly_surplus >= required_monthly
        
        return {
            "required_monthly_contribution": round(required_monthly, 2),
            "is_achievable": is_achievable,
            "recommended_adjustment": None if is_achievable else round(required_monthly - avg_monthly_surplus, 2)
        }
