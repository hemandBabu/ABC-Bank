from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db, init_db, Account, Transaction

app = FastAPI(title="ABC Banking Management System")

@app.on_event("startup")
def startup_event():
    init_db()

# --- Pydantic Schemas ---
class AccountCreate(BaseModel):
    account_number: str
    owner_name: str
    initial_deposit: float = 0.0

class TransactionRequest(BaseModel):
    account_number: str
    amount: float

class TransferRequest(BaseModel):
    sender_account_number: str
    receiver_account_number: str
    amount: float

# --- API Endpoints ---
@app.post("/api/accounts/create", summary="Create Account")
def create_account(data: AccountCreate, db: Session = Depends(get_db)):
    existing = db.query(Account).filter(Account.account_number == data.account_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Account number already exists.")
    
    new_account = Account(
        account_number=data.account_number,
        owner_name=data.owner_name,
        balance=data.initial_deposit
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    
    if data.initial_deposit > 0:
        tx = Transaction(account_id=new_account.id, transaction_type="DEPOSIT", amount=data.initial_deposit)
        db.add(tx)
        db.commit()
        
    return {"message": "Account created successfully", "account_number": new_account.account_number, "balance": new_account.balance}

@app.get("/api/accounts/{account_number}", summary="Get Account Details")
def get_account(account_number: str, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.account_number == account_number).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found.")
    return {
        "account_number": account.account_number,
        "owner_name": account.owner_name,
        "balance": account.balance,
        "created_at": account.created_at
    }

@app.post("/api/transactions/deposit", summary="Deposit Funds")
def deposit(req: TransactionRequest, db: Session = Depends(get_db)):
    if req.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero.")
        
    account = db.query(Account).filter(Account.account_number == req.account_number).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found.")
        
    account.balance += req.amount
    db.add(Transaction(account_id=account.id, transaction_type="DEPOSIT", amount=req.amount))
    db.commit()
    
    return {"message": "Deposit successful", "new_balance": account.balance}

@app.post("/api/transactions/withdraw", summary="Withdraw Funds")
def withdraw(req: TransactionRequest, db: Session = Depends(get_db)):
    if req.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero.")
        
    account = db.query(Account).filter(Account.account_number == req.account_number).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found.")
        
    if account.balance < req.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds.")
        
    account.balance -= req.amount
    db.add(Transaction(account_id=account.id, transaction_type="WITHDRAW", amount=req.amount))
    db.commit()
    
    return {"message": "Withdrawal successful", "new_balance": account.balance}

@app.post("/api/transactions/transfer", summary="Transfer Between Accounts")
def transfer(req: TransferRequest, db: Session = Depends(get_db)):
    if req.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero.")
        
    sender = db.query(Account).filter(Account.account_number == req.sender_account_number).first()
    receiver = db.query(Account).filter(Account.account_number == req.receiver_account_number).first()
    
    if not sender or not receiver:
        raise HTTPException(status_code=404, detail="Sender or receiver account not found.")
        
    if sender.balance < req.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds in sender account.")
        
    sender.balance -= req.amount
    receiver.balance += req.amount
    
    db.add(Transaction(account_id=sender.id, transaction_type="TRANSFER_OUT", amount=req.amount))
    db.add(Transaction(account_id=receiver.id, transaction_type="TRANSFER_IN", amount=req.amount))
    db.commit()
    
    return {"message": "Transfer successful", "sender_balance": sender.balance, "receiver_balance": receiver.balance}
