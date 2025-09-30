# ✈️旅行管理アプリ（MVP / FastAPI）

旅の計画を、シンプルに。
行きたい場所・メモ・日程をひとつの画面で軽快に管理できるミニマムな旅行管理アプリ。
技術: FastAPI / SQLite / SQLAlchemy / Jinja2 / Bootstrap（jQuery は最小限）

## ① プロダクト概要（なにを作ったのか？）
- アプリ名：旅行管理APP
- 一言で：旅の計画・メモ・日程を一括管理する軽量な個人向け旅行プランナー
- できること（MVP）
  - 旅程（Trip）と項目（Item）の CRUD
  - 「行きたい」をカード表示で視認性よくストック
  - デモユーザーと種データを同梱 → 5 分以内に体験開始
  - ログイン必須／メール認証（開発環境は Mailtrap を使用）
※「持ち物チェック」「検索・タグ」は今後の拡張としてロードマップに明示（現行実装には未搭載）。

## ② 作成の背景（なぜ作ったのか？）
- 課題意識：YouTube / Instagram / TV で見たスポット名やお店がすぐに埋もれる。スマホのメモや SNS 保存が散在し、後から探しづらい。
- 想定ユーザー：週末や連休に国内旅行を楽しむ個人。SNSで情報収集し、PC でも計画をざっくり整理したい人。
- モチベーション：
  - 自分専用で「行きたい」を気軽に貯められる定位置が欲しい
  - エンジニア転向ポートフォリオとして、最小構成でサクッと動く実用品を作り切る
    
## ③ 解決したい課題（どこに課題があるか？）
- 情報が散在：メモ / SNS 保存 / ブックマーク…保管場所が複数で迷子
- 目的がぶれる：「行きたい」だけのリストと、実際の旅程が混在して管理しづらい
- 入力が面倒：思いついたときにすぐ書けないと記録が続かない
  
仮説：ログイン後に「最小入力」「カード表示」が揃い、デモユーザーで即体験できれば、
“記録 → 見返し → 旅程化” が継続しやすくなる。

## ④ 解決アプローチ（どうやって解決したか？）
- 機能設計（MVP）
  - Trip（旅程）・Item（項目）に絞った最小データ構造
  - 画面は 一覧 → 詳細 の 2 階層で迷わない導線
  - カード UIで「行きたい」を視認性高くストック
  - 種データ投入スクリプト（scripts/seed.py）で審査体験を5分化
- 画面構成／UX
  - Bootstrap によるレスポンシブ・カードレイアウト
  - 必須バリデーション／エラー表示・Enter確定等で入力摩擦を最小化
  - jQuery を最小限に留め、ページ遷移をシンプルに
- 技術選定
  - FastAPI + SQLite + Jinja2（学習コストと審査体験のバランス）
  - SQLAlchemy（移行容易・保守性）／passlib（ハッシュ）／python-dotenv
  - メール認証は開発で Mailtrap を使用（本番は環境変数で切替）

## ⑤ 工夫ポイント（実装で意識した点）
- UI/UX
  - “3クリック以内で目的の旅程へ”を指標に導線設計
  - カード + バッジで状態を即時把握（例：「行きたい」/「済」等、今後拡張前提）
  - キーボード操作とモバイル入力のしやすさ（フォーカス・タップ幅）
- パフォーマンス／データ
  - 必要箇所で eager load し N+1 を抑制
  - SQLite を既定にしゼロ依存で起動、将来 MySQL へ移行可能な ORM 設計
- エラー処理／信頼性
  - 必須チェック・長さ制限・パターン等のバリデーション
  - 400/404 の簡易エラーページ、フォーム再表示時の入力保持
- 認証・セキュリティ（MVP 範囲）
  - ログイン必須／メール認証（実装済）、パスワードは passlib でハッシュ化
  - Jinja2 autoescape と基本的な入力検証
  - .env を Git 追跡除外、開発 SMTP は Mailtrap を使用

## ⑥ 学びと今後の改善点（振り返り・展望）
- 学び
  - FastAPI の依存性注入・ルーティング設計、Pydantic モデル設計
  - 審査体験を意識した 種データ と ゼロ依存（SQLite） の価値
  - 「メモ化アプリ」継続利用の鍵は入力摩擦の最小化と視認性
- 反省
  - 初期の画面仕様が曖昧で一部手戻り → ワイヤーフレーム先行の重要性を再確認
  - 権限・監査ログなどはMVPで割り切り（今後拡張）
- ロードマップ（次にやること）
  - パスワードリセット（メール + トークン）
  - CSRF 対策と Cookie 属性強化（Secure / HttpOnly / SameSite）
  - MySQL 化 と検索用 インデックス設計
  - I18N（JP/EN/ZH） と A11y（キーボード操作・コントラスト）
  - 検索・タグ（軽量版）、持ち物チェック（チェックリスト方式）
  - テスト整備（pytest）＋ CI（GitHub Actions）
  - 限定公開デモ動画（README へ時間コード付きで掲載）

## 🚀 クイックスタート（Windows PowerShell）

```ps1
# 1) 取得 & 移動
git clone https://github.com/sauwawa/travel-manager-fastapi.git
cd .\travel-manager-fastapi

# 2) 仮想環境
python -m venv .venv
.\.venv\Scripts\Activate

# 3) 依存関係
pip install --upgrade pip
pip install -r requirements.txt

# 4) 環境変数（例）
Copy-Item .env.example .env

# 5) DB（SQLite を既定に）
$env:DATABASE_URL="sqlite:///./app.db"

# 6) シードデータ投入
python .\scripts\seed.py

# 7) 起動
python -m uvicorn app.main:app --reload

- アプリ UI：http://127.0.0.1:8000/
- API（Swagger）：http://127.0.0.1:8000/docs
- デモログイン：demo@example.com / Demo#2025（種データ投入後に利用可）
```

## 🖼 スクリーンショット  
![Login](docs/images/login.png)
![Trips List](docs/images/trips-list.png)
![Trip Detail](docs/images/trip-detail.png)

## 🧱 技術スタック
- Backend：FastAPI / SQLAlchemy / Uvicorn
- Template：Jinja2（Bootstrap 5）
- DB：SQLite（既定） / MySQL（切替可）
- Auth：passlib（ハッシュ化）
- Others：python-dotenv / Mailtrap（開発でのメール確認）

## 🗃 ディレクトリ構成
```text
app/
  main.py
  models.py
  routers/
  templates/
  i18n/
scripts/
  seed.py
docs/
  images/
.env.example
requirements.txt
README.md
```
## 🔐 セキュリティ注意点
- .env やシークレットは コミットしない（.gitignore 済み）
- パスワードは ハッシュ化（passlib）
- Jinja2 の autoescape、基本的な 入力検証
- 本番運用時は Cookie 属性（Secure/HttpOnly/SameSite）を適切化

## 📜 ライセンス
MIT

## 🤖 AI アシストの透明性
本プロジェクトの一部のコードおよび README は ChatGPT を活用して作成・整形しています。
最終的な設計・検証・動作確認は開発者本人が実施しており、AI を適切に使い分ける実務力を重視しています。
