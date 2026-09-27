import pandas as pd
from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from connector import get_db, init_db, DBTransaction
from ai_engine import UnifiedFinancialAI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Modular Financial AI Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ai_engine = UnifiedFinancialAI()

@app.on_event("startup")
def startup_event():
    init_db()

class TransactionInput(BaseModel):
    user_id: str
    amount: float
    hour_of_day: int
    day_of_week: int

class CashFlowInput(BaseModel):
    daily_balances: list[float]

class GoalInput(BaseModel):
    current_savings: float
    target_amount: float
    target_months: int
    avg_monthly_surplus: float

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/transactions/evaluate")
def evaluate_tx(tx: TransactionInput, db: Session = Depends(get_db)):
    db_tx = DBTransaction(user_id=tx.user_id, amount=tx.amount, hour_of_day=tx.hour_of_day, day_of_week=tx.day_of_week)
    db.add(db_tx)
    db.commit()
    
    user_txs = db.query(DBTransaction).filter(DBTransaction.user_id == tx.user_id).all()
    if len(user_txs) > 3:
        df = pd.DataFrame([{"amount": t.amount, "hour_of_day": t.hour_of_day, "day_of_week": t.day_of_week} for t in user_txs])
        ai_engine.train_behavioral_profile(df)
        
    return ai_engine.evaluate_transaction(tx.dict())

@app.post("/api/cashflow/forecast")
def forecast(data: CashFlowInput):
    return ai_engine.forecast_cash_flow(data.daily_balances)

@app.post("/api/goals/calculate")
def goal_calc(goal: GoalInput):
    return ai_engine.calculate_goal(goal.current_savings, goal.target_amount, goal.target_months, goal.avg_monthly_surplus)
