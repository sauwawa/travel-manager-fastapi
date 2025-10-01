# ✈️ 旅行管理アプリ（MVP / FastAPI）

旅の計画を、シンプルに。
行きたい場所・メモ・日程をひとつの画面で軽快に管理できるミニマムな旅行管理アプリ。
技術: FastAPI / SQLite / SQLAlchemy / Jinja2 / Bootstrap（jQuery は最小限）

---

## ① プロダクト概要（なにを作ったのか？）
- アプリ名：旅行管理アプリ
- 一言で：旅の計画・メモ・日程を一括管理する軽量な個人向け旅行プランナー
- **できること（MVP）**
  - 旅程（Trip）と項目（Item）の **CRUD**
  - 「行きたい」を**カード表示**で視認性よくストック
  - **多言語対応（日本語 / 英語 / 繁體中文 / 简体中文）**（右上セレクターで切替）
  - **デモユーザー**と**シードデータ**を同梱 → **5 分以内に体験開始**
  - **ログイン必須／メール認証**（開発環境は **Mailtrap** を使用）

> ※「持ち物チェック」「検索・タグ」は今後の拡張としてロードマップに明示（現行実装には未搭載）。

---

## ② 作成の背景（なぜ作ったのか？）
- 課題意識：YouTube / Instagram / TV で見たスポット名やお店がすぐに埋もれる。スマホのメモや SNS 保存が散在し、後から探しづらい。
- 想定ユーザー：週末や連休に国内旅行を楽しむ個人。SNSで情報収集し、PC でも計画をざっくり整理したい人。
- モチベーション：
  - 自分専用で「行きたい」を気軽に貯められる定位置が欲しい
  - エンジニア転向ポートフォリオとして、最小構成でサクッと動く実用品を作り切る

---

## ③ 解決したい課題（どこに課題があるか？）
- 情報が散在：メモ / SNS 保存 / ブックマーク…保管場所が複数で迷子
- 目的がぶれる：「行きたい」だけのリストと、実際の旅程が混在して管理しづらい
- 入力が面倒：思いついたときにすぐ書けないと記録が続かない
  
**仮説**：ログイン後に「**最小入力**」「**カード表示**」が揃い、**デモユーザーで即体験**できれば、  
“記録 → 見返し → 旅程化” が継続しやすくなる。

---

## ④ 解決アプローチ（どうやって解決したか？）
- **機能設計（MVP）**
  - Trip（旅程）・Item（項目）に絞った最小データ構造
  - 画面は **一覧 → 詳細** の 2 階層で迷わない導線
  - **カード UI**で「行きたい」を視認性高くストック
  - **シードデータ投入スクリプト**（scripts/seed.py）で審査体験を5分化
- **画面構成／UX**
  - Bootstrap によるレスポンシブ・カードレイアウト
  - 必須バリデーション／エラー表示・Enter確定等で入力摩擦を最小化
  - jQuery を最小限に留め、ページ遷移をシンプルに
- **技術選定**
  - FastAPI + SQLite + Jinja2（学習コストと審査体験のバランス）
  - SQLAlchemy（移行容易・保守性）／passlib（ハッシュ）／python-dotenv
  - メール認証は開発で Mailtrap を使用（本番は環境変数で切替）

---

## 🌐 多言語対応（I18N）
- **対応言語**：日本語（既定）／英語（EN）／繁體中文（ZH-TW）／简体中文（ZH-CN）
- **切替方法**：
  - 画面右上の言語セレクター（`JP | EN | ZH-TW | ZH-CN`）で即時切替
  - または URL クエリ：`?lang=jp` / `en` / `zh-tw` / `zh-cn`
- **実装方式**：Jinja2 テンプレート + 辞書（`L["キー"]`）。未翻訳キーは既定言語にフォールバック。
- **既定言語の設定**：`.env` の `DEFAULT_LANG` で制御（例：`DEFAULT_LANG=jp`）
- **テンプレ例**：

```jinja2
<h1>{{ L["trips_title"] }}</h1>
<button>{{ L["add_item"] }}</button>
```
---

## ⑤ 工夫ポイント（実装で意識した点）
- **UI/UX**
  - “**3クリック以内**で目的の旅程へ”を指標に導線設計
  - **カード + バッジ**で状態を即時把握（例：「行きたい」/「済」等、今後拡張前提）
  -  **多言語 UI を辞書分離**（テンプレ側は `L["キー"]` 参照）で保守性を確保
  - キーボード操作とモバイル入力のしやすさ（フォーカス・タップ幅）
- **パフォーマンス／データ**
  - 必要箇所で eager loading を採用し **N+1** を抑制
  - SQLite を既定にし**ゼロ依存で起動**、将来 **MySQL へ移行**可能な ORM 設計
- **エラー処理／信頼性**
  - **必須チェック・長さ制限・パターン**等のバリデーション
  - **400/404** の簡易エラーページ、フォーム再表示時の**入力保持**
- **認証・セキュリティ（MVP 範囲）**
  - **ログイン必須／メール認証（実装済）**、パスワードは **passlib** でハッシュ化
  - Jinja2 の **autoescape** と基本的な**入力検証**
  - `.env` を **Git 追跡除外**、開発 SMTP は **Mailtrap** を使用

---

## ⑥ 学びと今後の改善点（振り返り・展望）
- **学び**
  - FastAPI の**依存性注入・ルーティング設計**、Pydantic モデル設計
  - 審査体験を意識した **シードデータ** と **ゼロ依存（SQLite）** の価値
  - 「メモ化アプリ」継続利用の鍵＝**入力摩擦の最小化**と**視認性**
  
- **反省**
  - 初期の画面仕様が曖昧で一部**手戻り** → **ワイヤーフレーム先行**の重要性を再確認
  - 権限・監査ログなどは**MVP で割り切り**（今後拡張）
  
- **ロードマップ（次にやること → 中期の計画）**
> 方針：まず“安全に触れる”MVPの完成度（復旧・安全・再現性）を上げ、その後ユーザー価値の高い体験機能を段階投入します。  
> **Target** = 目標リリース、**Effort** = 規模感（S/M/L）。

 ### ✅ 直近（安定化・評価しやすさの向上）
1. **パスワードリセット**（メール + トークン）  
   - Target: `v0.1.1`　Effort: `S`
2. **CSRF 対策** と Cookie 属性強化（`Secure` / `HttpOnly` / `SameSite`）  
   - Target: `v0.1.1`　Effort: `S`
3. **テスト整備（pytest）＋ CI（GitHub Actions）**  
   - Target: `v0.1.2`　Effort: `M`（単体 → 主要ルートのE2E）

### 🧭 使い勝手（MVP拡張）
4. **検索・タグ（軽量版）**  
   - Target: `v0.1.3`　Effort: `M`
5. **持ち物チェック**（チェックリスト方式）  
   - Target: `v0.1.3`　Effort: `S`
6. **I18N 強化**（用語統一・未翻訳キー検知） と **A11y**（キーボード操作・コントラスト）  
   - Target: `v0.1.4`　Effort: `M`

### 🗄️ 基盤
7. **MySQL 化** と検索用 **インデックス設計**  
   - Target: `v0.2.0`　Effort: `M`

---

### 🗺️ 中期（計画中 / 未実装の将来機能）
- **地図表示（スポット可視化）** — Target: `v0.2.1`　Effort: `M`
- **旅行予定日の通知（メール）** — Target: `v0.2.2`　Effort: `M`
- **印刷・共有（PDF / 印刷 CSS / SNS）** — Target: `v0.3.0`　Effort: `M`
- **URL・QR コード招待 / 共同編集** — Target: `v0.3.1`　Effort: `L`

---

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

# 4) 環境変数（.env を作成）
Copy-Item .env.example .env

# 5) DB（SQLite を既定に）
$env:DATABASE_URL="sqlite:///./app.db"

# 6) シードデータ投入（デモユーザーとサンプル旅程）
python .\scripts\seed.py

# 7) 起動
python -m uvicorn app.main:app --reload
```

**`.env.example` の抜粋：**

```dotenv
APP_ENV=development
APP_BASE_URL=http://127.0.0.1:8000
DEFAULT_LANG=jp  # 既定言語: jp / en / zh-tw / zh-cn
DATABASE_URL=sqlite:///./app.db
```
- **アプリ UI**：<http://127.0.0.1:8000/>
- **API（Swagger）**：<http://127.0.0.1:8000/docs>
- **デモログイン**：`demo@example.com / Demo#2025`（シードデータ投入後に利用可）

---

## 🖼 スクリーンショット
![Login](docs/images/login.png)  
![Trips List](docs/images/trips-list.png)  
![Trip Detail](docs/images/trip-detail.png)

---

## 🎥 デモ動画（限定公開）

> 面接官向けの 2–3 分ダイジェスト。限定公開リンクで視聴できます。

- 視聴リンク（限定公開）：https://youtu.be/XXXXXXXXXXX
- 目次（時間コード）
  - 00:00 紹介（目的・技術スタック）
  - 00:15 ログイン（デモユーザー）
  - 00:45 旅程一覧（カード表示）
  - 01:10 旅程の新規作成（Trip / Item CRUD）
  - 01:40 多言語切替（JP / EN / ZH-TW / ZH-CN）
  - 02:00 API ドキュメント（/docs）
  - 02:15 まとめ（ロードマップ要点）

---

## 🧱 技術スタック
- **Backend**：FastAPI / SQLAlchemy / Uvicorn  
- **Template**：Jinja2（Bootstrap 5）  
- **DB**：SQLite（既定） / MySQL（切替可）  
- **Auth**：passlib（ハッシュ化）  
- **Others**：python-dotenv / Mailtrap（開発でのメール確認）

---

## 🗃 ディレクトリ構成

```text
app/
  main.py                 # FastAPI 起動エントリ
  models.py               # SQLAlchemy モデル
  mail.py                 # メール送信（Mailtrap 等）
  static/                 # CSS / JS / 画像（ビルド成果物は含めない）
    css/
    js/
    img/
  services/               # 業務ロジック層（DB操作の組み立て等）
  utils/                  # 共通ユーティリティ（バリデーション等）
  routers/                # 画面/API ルーティング
    __init__.py
    auth.py               # 認証・メール検証
    trips.py              # 旅程／項目 CRUD
    [...]
  templates/              # Jinja2 テンプレート
    base.html
    login.html
    register.html
    trip_list.html
    trip_detail.html
    trip_new.html
  i18n/                   # 多言語辞書（右上切替）
    __init__.py
    jp.py
    en.py
    zh_tw.py
    zh_cn.py
scripts/
  seed.py                 # デモユーザー＆サンプル旅程投入
docs/
  images/                 # README 用スクリーンショット
.env.example
requirements.txt
README.md
```
---

## 🔐 セキュリティ注意点
- `.env` やシークレットは **コミットしない**（`.gitignore` 済み）
- パスワードは **ハッシュ化**（passlib）
- Jinja2 の **autoescape**、基本的な **入力検証**
- 本番運用時は Cookie 属性（`Secure` / `HttpOnly` / `SameSite`）を適切化

---

## 付録：.gitignore

```gitignore
# Python / venv / キャッシュ
.venv/
__pycache__/
*.pyc
*.pyo
*.pyd
*.egg-info/
.pytest_cache/
.mypy_cache/

# 実行時に生成されるファイル
app.db
*.log

# カバレッジ / ビルド成果物（将来の自動化を想定）
.coverage
htmlcov/
dist/
build/

# フロント系（将来追加する場合に備え）
node_modules/

# 環境変数・秘密情報
.env
.env.local

# OS / エディタ
.DS_Store
Thumbs.db
.idea/
.vscode/
```

### 補足
- `services/`：ルータから呼ぶ**業務ロジック**（例：Trip 作成＋関連 Item の一括登録）
- `utils/`：**共通関数**（入力チェック、日時フォーマット等）
- `static/`：**手書き CSS/JS** や画像のみ（ビルド生成物や巨大アセットは**含めない**方針）
  
---

## 📜 ライセンス
MIT

---

## 🤖 AI アシストの透明性
本プロジェクトの一部のコードおよび README は **ChatGPT** を活用して作成・整形しています。  
**最終的な設計・検証・動作確認は開発者本人が実施**しており、AI を**適切に使い分ける実務力**を重視しています。
