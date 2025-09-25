# 旅行管理アプリ（MVP）

FastAPI + SQLite + Jinja2 で構成した最小ポートフォリオ。API と簡易UIを同梱しています。

## スクリーンショット
- トップ（行程一覧）
- 行程詳細（項目追加フォーム）

## セットアップ
```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

アクセス：
- アプリUI: http://127.0.0.1:8000/
- APIドキュメント（Swagger）: http://127.0.0.1:8000/docs

## 機能
- Trip（行程）CRUD の API（最小）
- 行程一覧／行程詳細（項目追加）UI
- 初回起動時、サンプルデータ投入

## 今後の拡張（例）
- 認証（ログイン）
- MySQL への切り替え
- React/HTMX 版フロントの追加
- 経費（Expense）管理、タグ、地図表示

## AIアシストの透明性
このプロジェクトの一部コードやREADMEは、GPT（ChatGPT）を用いて生成／整形しています。最終的な設計・検証・動作確認は私自身が行いました。
