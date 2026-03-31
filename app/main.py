# メインAPI
from fastapi import FastAPI, Depends
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine, Base
from app.db import models
from app.schemas import HealthCreate, UserCreate, UserLogin
from app.services.analysis import calculate_bmi, calculate_stats, calculate_trend, generate_weight_graph, generate_bmi_bar_chart
from app.services.auth import hash_password, verify_password, create_access_token, get_current_user


app = FastAPI()

# テーブル作成
Base.metadata.create_all(bind=engine)


# DBセッション
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
# ユーザー登録
@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed_pw = hash_password(user.password)
    
    new_user = models.User(
        username=user.username,
        password=hashed_pw
    )
    
    db.add(new_user)
    db.commit()
    return {"message": "ユーザー登録完了"}


# ログイン
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == form_data.username).first()
    
    if not db_user:
        return {"error": "ユーザーが存在しません"}
    
    if not verify_password(form_data.password, db_user.password):
        return {"error": "パスワードが違います"}
    
    token = create_access_token({"sub": db_user.username})
    
    return {"access_token": token}
        
        
# データ登録
@app.post("/records")
def create_record(data: HealthCreate, db: Session = Depends(get_db)):
    bmi = calculate_bmi(data.height, data.weight)
    
    record = models.HealthRecord(
        height=data.height,
        weight=data.weight,
        bmi=bmi
    )
    
    db.add(record)
    db.commit()
    db.refresh(record)
    
    return {
        "id": record.id,
        "bmi": round(bmi, 2)
    }
    
    
# 一覧取得
@app.get("/records")
def get_records(
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    return db.query(models.HealthRecord).all()


# 統計情報
@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    records = db.query(models.HealthRecord).all()
    return  calculate_stats(records)


# トレンド
@app.get("/trend")
def get_trend(db: Session = Depends(get_db)):
    records = db.query(models.HealthRecord).all()
    return calculate_trend(records)


# 折れ線＋点グラフ
@app.get("/graph/weight")
def weight_graph(db: Session = Depends(get_db)):
    records = db.query(models.HealthRecord).all()
    buf = generate_weight_graph(records)
    return StreamingResponse(buf, media_type="image/png")


# 棒グラフ
@app.get("/graph/bmi")
def bmi_graph(db: Session = Depends(get_db)):
    records = db.query(models.HealthRecord).all()
    buf = generate_bmi_bar_chart(records)
    return StreamingResponse(buf, media_type="image/png")