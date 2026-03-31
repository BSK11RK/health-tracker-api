# 分析ロジック
import pandas as pd
import matplotlib.pyplot as plt
import io, os
from datetime import datetime


GRAPH_DIR = "graphs"
os.makedirs(GRAPH_DIR, exist_ok=True)

def calculate_bmi(height: float, weight: float):
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    return bmi


def calculate_stats(records):
    # records → dictへ変換
    data = [
        {
            "height": r.height,
            "weight": r.weight,
            "bmi": r.bmi
        }
        for r in records
    ]
    
    # pandasで分析
    df = pd.DataFrame(data)
    if df.empty:
        return {"message": "データがありません"}
    
    return {
        "count": len(df),
        "mean_bmi": round(df["bmi"].mean(), 2),
        "median_bmi": round(df["bmi"].median(), 2),
        "max_bmi": round(df["bmi"].max(), 2),
        "min_bmi": round(df["bmi"].min(), 2)
    }
    
    
def calculate_trend(records):
    if len(records) < 2:
        return {"message": "データが不足しています"}
    
    # 日付順にソート
    sorted_records = sorted(records, key=lambda x: x.created_at)
    
    first = sorted_records[0]
    last = sorted_records[1]
    
    weight_diff = last.weight - first.weight
    bmi_diff = last.bmi - first.bmi
    
    
    return {
        "start_date": first.created_at,
        "end_date": last.created_at,
        "weight_change": round(weight_diff, 2),
        "bmi_change": round(bmi_diff, 2),
        "trend": "increase" if weight_diff > 0 else "decrease"
    }
    
    
def generate_weight_graph(records):
    if len(records) == 0:
        return None
    
    # 日付順にソート
    records = sorted(records, key=lambda x: x.created_at)
    
    dates = [r.created_at for r in records]
    weights = [r.weight for r in records]
    
    # グラフ作成
    plt.figure()
    
    # 折れ線＋点
    plt.plot(dates, weights, marker= "o")
    
    plt.xlabel("Date")
    plt.ylabel("Weight")
    plt.title("Weight Trend")
    
    # 画像をメモリに保存
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    
    buf.seek(0)
    return buf


def generate_bmi_bar_chart(records):
    if len(records) == 0:
        return None
    
    records = sorted(records, key=lambda x: x.created_at)
    
    dates = [r.created_at.strftime("%m-%d") for r in records]
    bmis = [r.bmi for r in records]
    
    plt.figure()
    plt.bar(dates, bmis)
    
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.title("BMI Bar Chart")
    
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    
    buf.seek(0)
    return buf


def save_weight_graph(records, user_id: int):
    if len(records) == 0:
        return None
    
    records = sorted(records, key=lambda x: x.created_at)
    
    dates = [r.created_at for r in records]
    weights = [r.weight for r in records]
    
    plt.figure()
    plt.plot(dates, weights, marker="o")
    
    plt.xlabel("Date")
    plt.ylabel("Weight")
    plt.title("Weight Trend")
    
    # ファイル名
    filename = f"weight_user_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    file_path = f"{GRAPH_DIR}/{filename}"
    
    plt.savefig(file_path)
    plt.close()
    return file_path