# メインAPI
from fastapi import FastAPI, Depends
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import csv

from app.db.database import SessionLocal, engine, Base
from app.db import models
from app.schemas import HealthCreate, UserCreate, UserLogin
from app.services.analysis import calculate_bmi, calculate_stats, calculate_trend, generate_weight_graph, generate_bmi_bar_chart, save_weight_graph
from app.services.auth import hash_password, verify_password, create_access_token, get_current_user


app = FastAPI()

app.mount("/graphs", StaticFiles(directory="graphs"), name="graphs")

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
@app.post("/register", tags=["Auth"])
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
@app.post("/login", tags=["Auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == form_data.username).first()
    
    if not db_user:
        return {"error": "ユーザーが存在しません"}
    
    if not verify_password(form_data.password, db_user.password):
        return {"error": "パスワードが違います"}
    
    token = create_access_token({"sub": db_user.username})
    
    return {"access_token": token}
        

# データ一覧取得
@app.get("/records", tags=["Records"])
def get_records(
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    records = db.query(models.HealthRecord) \
        .filter(models.HealthRecord.user_id == user.id).all()
        
    return records

   
# データ登録
@app.post("/records", tags=["Records"])
def create_record(
    data: HealthCreate, 
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    bmi = calculate_bmi(data.height, data.weight)
    
    record = models.HealthRecord(
        height=data.height,
        weight=data.weight,
        bmi=bmi,
        age=data.age,
        gender=data.gender,
        user_id=user.id
    )
    
    db.add(record)
    db.commit()
    db.refresh(record)
    
    return {"bmi": round(bmi, 2)}


# 更新機能
@app.put("/records/{record_id}", tags=["Records"])
def update_record(record_id: int, data: HealthCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    record = db.query(models.HealthRecord) \
        .filter(models.HealthRecord.id == record_id) \
        .filter(models.HealthRecord.user_id == user.id).first()
        
    if not record:
        return {"error": "見つかりません"}
    
    record.height = data.height
    record.weight = data.weight
    record.bmi = calculate_bmi(data.height, data.weight)
    
    db.commit()
    return {"message": "更新完了"}


# 削除機能
@app.delete("/records/{record_id}", tags=["Records"])
def deleye_record(record_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    record = db.query(models.HealthRecord) \
        .filter(models.HealthRecord.id == record_id) \
        .filter(models.HealthRecord.user_id == user.id).first()
        
    if not record:
        return {"error": "見つかりません"}
    
    db.delete(record)
    db.commit()
    return {"message": "削除完了"}


# CSV読み込みAPI
@app.post("/import", tags=["Import"])
def import_data(db: Session = Depends(get_db), user = Depends(get_current_user)):
    with open("data/sample_data.csv", newline="") as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            bmi = calculate_bmi(float(row["height"]), float(row["weight"]))
            
            record = models.HealthRecord(
                height=float(row["height"]),
                weight=float(row["weight"]),
                bmi=bmi,
                age=int(row["age"]),
                gender=row["gender"],
                user_id=user.id
            )
            
            db.add(record)
        db.commit()
    return {"message": "データ登録完了"}


# 統計情報
@app.get("/stats", tags=["Analytics"])
def get_stats(db: Session = Depends(get_db)):
    records = db.query(models.HealthRecord).all()
    return  calculate_stats(records)


# トレンド
@app.get("/trend", tags=["Analytics"])
def get_trend(db: Session = Depends(get_db)):
    records = db.query(models.HealthRecord).all()
    return calculate_trend(records)


# 折れ線＋点グラフ
@app.get("/graph/weight",tags=["Graph"])
def weight_graph(db: Session = Depends(get_db)):
    records = db.query(models.HealthRecord).all()
    buf = generate_weight_graph(records)
    return StreamingResponse(buf, media_type="image/png")


# 棒グラフ
@app.get("/graph/bmi", tags=["Graph"])
def bmi_graph(db: Session = Depends(get_db)):
    records = db.query(models.HealthRecord).all()
    buf = generate_bmi_bar_chart(records)
    return StreamingResponse(buf, media_type="image/png")


# グラフ保存
@app.get("/graph/save", tags=["Graph"])
def save_graph(db: Session = Depends(get_db), user = Depends(get_current_user)):
    records = db.query(models.HealthRecord) \
        .filter(models.HealthRecord.user_id == user.id).all()
        
    path = save_weight_graph(records, user.id)
    
    return {"file_path": path, "url": f"http://localhost:8000/{path}"}