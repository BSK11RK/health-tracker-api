# Health Tracker API

## 概要

健康データ（身長・体重・年齢・性別）を記録し、BMIの計算・統計分析・トレンド分析・グラフ可視化を行うAPIです。
JWT認証を用いてユーザーごとにデータを分離しています。

---

## 主な機能

* ユーザー登録 / ログイン（JWT認証）
* 健康データの登録・取得・更新・削除（CRUD）
* BMI計算
* 統計分析（平均・中央値・最大・最小）
* トレンド分析（増減）
* グラフ生成（折れ線・棒グラフ）
* グラフ画像の保存（日時付きファイル名）
* 保存したグラフのURLアクセス
* CSVによるサンプルデータの一括登録

---

## 使用技術

* Python
* FastAPI
* SQLite
* SQLAlchemy
* JWT認証
* matplotlib
* pandas
* Docker / Docker Compose

---

## ディレクトリ構成

.
├── app/
├── data/        # DBファイル
├── graphs/      # グラフ画像
├── sample_data.csv
├── Dockerfile
├── docker-compose.yml
└── README.md

---

## セットアップ方法

### ローカル環境

pip install -r requirements.txt
uvicorn app.main:app --reload

---

### Docker

docker-compose up --build

---

## API一覧

### 認証

* POST /register
* POST /login

### データ

* GET /records
* POST /records
* PUT /records/{id}
* DELETE /records/{id}

### データインポート

* POST /import

### 分析

* GET /stats
* GET /trend

### グラフ

* GET /graph/weight
* GET /graph/bmi
* GET /graph/save

---

## サンプルデータ

sample_data.csvを使用して複数ユーザーの健康データを一括登録できます。

---

## 工夫した点

* JWT認証によりユーザーごとにデータを分離
* 年齢・性別を追加し、より実用的なデータ構造に改善
* データ分析機能（統計・トレンド）を実装
* グラフを画像として保存し、URLでアクセス可能にした
* CSVインポートにより大量データの検証を可能にした
* Docker環境で簡単に起動できるように構築

---

## 今後の改善点

* PostgreSQL対応
* デプロイ（クラウド環境）
* AIによる健康アドバイス機能