# メインAPI
from fastapi import FastAPI, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine, Base
from app.db import models
from app.schemas import HealthCreate
from app.services.analysis import calculate_bmi, calculate_stats, calculate_trend, generate_weight_graph, generate_bmi_bar_chart


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
        
        
# データ登録
@app.post("/records")
def create_record(data: HealthCreate, db: Session = Depends(get_db)):
    bmi = calculate_bmi(data.heigth, data.weight)
    
    record = models.HealthRecord(
        height=data.heigth,
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
def get_records(db: Session = Depends(get_db)):
    records = db.query(models.HealthRecord).all()
    return records


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