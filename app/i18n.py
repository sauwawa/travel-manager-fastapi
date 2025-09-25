# -*- coding: utf-8 -*-
# i18n.py
# 日本語を既定とする簡易辞書。Cookie "lang" で切替。
# 画面テキストは全てこの辞書経由で出す方針。

from typing import Dict

LANGS = {"ja", "en", "zh-Hant", "zh-Hans"}

# 把舊寫法或簡寫統一到四語代碼
NORMALIZE = {
    "zh": "zh-Hant",
    "zh_TW": "zh-Hant", "zh-TW": "zh-Hant", "tw": "zh-Hant",
    "zh_CN": "zh-Hans", "zh-CN": "zh-Hans", "cn": "zh-Hans",
    "zh-Hant": "zh-Hant", "zh-Hans": "zh-Hans",
}

def normalize_lang(code: str | None) -> str:
    c = (code or "").strip()
    c = NORMALIZE.get(c, c)
    return c if c in LANGS else "ja"

def get_lang(request) -> str:
    # Cookie の lang を参照、なければ ja。正規化して返す
    raw = request.cookies.get("lang", "ja")
    return normalize_lang(raw)

STRINGS: Dict[str, Dict[str, str]] = {
    # アプリ名・ナビ
    "app_title": {"ja": "旅行管理", "en": "Travel Manager", "zh-Hant": "旅行管理", "zh-Hans": "旅行管理"},
    "owner_app_fmt": {  # {name} と {app} を差し込み
        "ja": "{name} さん の {app}",
        "en": "{name}'s {app}",
        "zh-Hant": "{name}的{app}",
        "zh-Hans": "{name}的{app}",
    },
    "home": {"ja":"ホーム","en":"Home","zh-Hant":"主頁","zh-Hans":"主页"},
    "trip_list": {"ja":"旅行一覧","en":"Trips","zh-Hant":"旅行列表","zh-Hans":"旅行列表"},
    "new": {"ja":"新規作成","en":"New","zh-Hant":"新增","zh-Hans":"新增"},
    "edit": {"ja":"編集","en":"Edit","zh-Hant":"編輯","zh-Hans":"编辑"},
    "delete": {"ja":"削除","en":"Delete","zh-Hant":"刪除","zh-Hans":"删除"},
    "items": {"ja":"旅程項目","en":"Itinerary Items","zh-Hant":"行程項目","zh-Hans":"行程项目"},
    "back": {"ja":"戻る","en":"Back","zh-Hant":"返回","zh-Hans":"返回"},
    "save": {"ja":"保存","en":"Save","zh-Hant":"儲存","zh-Hans":"保存"},
    "create": {"ja":"作成","en":"Create","zh-Hant":"建立","zh-Hans":"建立"},
    "cancel": {"ja":"キャンセル","en":"Cancel","zh-Hant":"取消","zh-Hans":"取消"},
    "logout": {"ja":"ログアウト","en":"Logout","zh-Hant":"登出","zh-Hans":"退出"},
    "login": {"ja":"ログイン","en":"Login","zh-Hant":"登入","zh-Hans":"登录"},
    "register": {"ja":"新規登録","en":"Sign up","zh-Hant":"註冊","zh-Hans":"注册"},
    "password_confirm": {"ja": "パスワード（確認）","en": "Password (confirm)","zh-Hant": "密碼（確認）","zh-Hans": "密码（确认）"},
    "error_password_mismatch": {"ja": "パスワードと確認が一致しません。","en": "Password and confirmation do not match.","zh-Hant": "密碼與確認不一致。","zh-Hans": "密码与确认不一致。"},

    "sort_hint": {
        "ja":"✔ 旅行/項目をドラッグして並べ替えできます。離すと自動保存されます。",
        "en":"✔ Drag trips/items to reorder. Changes save automatically.",
        "zh-Hant":"✔ 旅行/項目可拖曳調整順序，放開即自動儲存。",
        "zh-Hans":"✔ 旅行/项目可拖拽调整顺序，放开即自动保存。",
    },


    # フィールド（label / placeholder）
    "title_label":{"ja":"タイトル","en":"Title","zh-Hant":"標題","zh-Hans":"标题"},
    "title_ph":{"ja":"タイトル","en":"Title","zh-Hant":"標題","zh-Hans":"标题"},
    "date_label":{"ja":"日付","en":"Date","zh-Hant":"日期","zh-Hans":"日期"},
    "date_ph":{"ja":"日付 (YYYY-MM-DD・任意)","en":"Date (YYYY-MM-DD, optional)","zh-Hant":"日期（YYYY-MM-DD，選填）","zh-Hans":"日期（YYYY-MM-DD，选填）"},
    "time_label":{"ja":"時間","en":"Time","zh-Hant":"時間","zh-Hans":"时间"},
    "time_ph":{"ja":"時間 例: 09:30","en":"Time e.g. 09:30","zh-Hant":"時間 例：09:30","zh-Hans":"时间 例：09:30"},
    "note_label":{"ja":"メモ","en":"Note","zh-Hant":"備註","zh-Hans":"备注"},
    "note_ph":{"ja":"メモ (任意)","en":"Note (optional)","zh-Hant":"備註（選填）","zh-Hans":"备注（选填）"},
    "start_date_label":{"ja":"開始日","en":"Start","zh-Hant":"開始日","zh-Hans":"开始日"},
    "start_date_ph":{"ja":"開始日 (YYYY-MM-DD・任意)","en":"Start (YYYY-MM-DD, optional)","zh-Hant":"開始日（YYYY-MM-DD，選填）","zh-Hans":"开始日（YYYY-MM-DD，选填）"},
    "end_date_label":{"ja":"終了日","en":"End","zh-Hant":"結束日","zh-Hans":"结束日"},
    "end_date_ph":{"ja":"終了日 (YYYY-MM-DD・任意)","en":"End (YYYY-MM-DD, optional)","zh-Hant":"結束日（YYYY-MM-DD，選填）","zh-Hans":"结束日（YYYY-MM-DD，选填）"},
    "description_label":{"ja":"説明","en":"Description","zh-Hant":"說明","zh-Hans":"说明"},
    "description_ph":{"ja":"説明 (任意)","en":"Description (optional)","zh-Hant":"說明（選填）","zh-Hans":"说明（选填）"},

    # 空表示・削除確認
    "no_trips":{"ja":"まだ旅行がありません。右上の「新規作成」から追加してください。","en":"No trips yet. Click “New” to add one.","zh-Hant":"尚未有旅行，請點右上「新增」。","zh-Hans":"尚未有旅行，请点右上“新增”。"},
    "no_items":{"ja":"まだ項目がありません。","en":"No items yet.","zh-Hant":"尚未有項目。","zh-Hans":"尚未有项目。"},
    "delete_trip":{"ja":"旅行を削除","en":"Delete Trip","zh-Hant":"刪除旅行","zh-Hans":"删除旅行"},
    "delete_trip_confirm":{"ja":"この旅行とすべての項目を削除しますか？","en":"Delete this trip and all items?","zh-Hant":"要刪除整個旅行與所有項目嗎？","zh-Hans":"要删除整个旅行与所有项目吗？"},
    "delete_item_confirm":{"ja":"この項目を削除しますか？","en":"Delete this item?","zh-Hant":"要刪除這個項目嗎？","zh-Hans":"要删除这个项目吗？"},

    # 言語選択
    "lang_ja":{"ja":"日本語","en":"Japanese","zh-Hant":"日文","zh-Hans":"日文"},
    "lang_en":{"ja":"英語","en":"English","zh-Hant":"英文","zh-Hans":"英文"},
    "lang_zh_hant":{"ja":"繁體字","en":"Chinese (Traditional)","zh-Hant":"繁體中文","zh-Hans":"繁体中文"},
    "lang_zh_hans":{"ja":"簡体字","en":"Chinese (Simplified)","zh-Hant":"簡體中文","zh-Hans":"简体中文"},

    # 認証フォーム
    "login_title":{"ja":"ログイン","en":"Login","zh-Hant":"登入","zh-Hans":"登录"},
    "register_title":{"ja":"新規登録","en":"Sign up","zh-Hant":"註冊","zh-Hans":"注册"},
    "login_id":{"ja":"Login ID","en":"Login ID","zh-Hant":"Login ID","zh-Hans":"Login ID"},
    "password":{"ja":"パスワード","en":"Password","zh-Hant":"密碼","zh-Hans":"密码"},
    "register_submit":{"ja":"登録","en":"Sign up","zh-Hant":"註冊","zh-Hans":"注册"},
    "to_login":{"ja":"ログインへ","en":"Go to login","zh-Hant":"前往登入","zh-Hans":"前往登录"},
    "to_register":{"ja":"新規登録へ","en":"Go to sign up","zh-Hant":"前往註冊","zh-Hans":"前往注册"},

    # ヒント・検証
    "hint_login_id":{"ja":"英数字 5～20 文字","en":"Alphanumeric 5–20 chars","zh-Hant":"英數 5–20 字元","zh-Hans":"英数 5–20 字符"},
    "hint_password":{"ja":"8～20 文字","en":"8–20 chars","zh-Hant":"8–20 字元","zh-Hans":"8–20 字符"},

    # エラー
    "err_login_bad":{"ja":"ID またはパスワードが違います。","en":"Invalid ID or password.","zh-Hant":"ID 或密碼錯誤。","zh-Hans":"ID 或密码错误。"},
    "err_id_used":{"ja":"この Login ID は既に使用されています。","en":"Login ID already in use.","zh-Hant":"此 Login ID 已被使用。","zh-Hans":"该 Login ID 已被使用。"},
    "err_id_format":{"ja":"Login ID は英数字 5～20 文字で入力してください。","en":"Login ID must be alphanumeric (5–20 chars).","zh-Hant":"Login ID 需為英數 5–20 字元。","zh-Hans":"Login ID 须为英数 5–20 字符。"},
    "err_pw_format":{"ja":"パスワードは 8～20 文字で入力してください。","en":"Password must be 8–20 chars.","zh-Hant":"密碼需為 8–20 字元。","zh-Hans":"密码须为 8–20 字符。"},
}
def get_lang(request) -> str:
    # Cookie の lang を参照、無ければ ja
    code = request.cookies.get("lang", "ja")
    return code if code in LANGS else "ja"

def get_L(lang: str):
    # 未翻訳は ja をフォールバック
    return {k: (v.get(lang) or v.get("ja") or k) for k, v in STRINGS.items()}

# パスワード可視化トグルの文言
STRINGS.update({
    "show_pw": {"ja":"パスワードを表示","en":"Show password","zh-Hant":"顯示密碼","zh-Hans":"显示密码"},
    "hide_pw": {"ja":"パスワードを非表示","en":"Hide password","zh-Hant":"隱藏密碼","zh-Hans":"隐藏密码"},
    "email": {"ja":"メールアドレス","en":"Email","zh-Hant":"電郵地址","zh-Hans":"电子邮箱"},
    "email_confirm": {"ja":"メールアドレス（確認）","en":"Email (confirm)","zh-Hant":"電郵地址（確認）","zh-Hans":"电子邮箱（确认）"},
    "error_email_mismatch": {"ja":"メールが一致しません。","en":"Emails do not match.","zh-Hant":"Email 不一致。","zh-Hans":"Email 不一致。"},
    "resend_wait": {"ja":"再送信はしばらくお待ちください。","en":"Please wait before resending.","zh-Hant":"請稍候再重送。","zh-Hans":"请稍候再重送。"},
    "send_code": {"ja":"認証コード送信","en":"Send code","zh-Hant":"寄送驗證碼","zh-Hans":"发送验证码"},
    "code": {"ja":"認証コード","en":"Verification code","zh-Hant":"驗證碼","zh-Hans":"验证码"},
    "code_hint": {"ja":"メールに届いた6桁コード（15分で無効）","en":"6-digit code from email (expires in 15 min)","zh-Hant":"Email 6碼驗證碼（15分鐘內有效）","zh-Hans":"Email 6位验证码（15分钟内有效）"},
    "code_sent": {"ja":"認証コードを送信しました。メールを確認してください。","en":"Verification code has been sent. Please check your email.","zh-Hant":"已寄出驗證碼到您提供的電郵地址，請查收。","zh-Hans":"已发送验证码到您提供的電子邮箱，请查收。"},
    "error_code_invalid_or_expired": {"ja":"認証コードが無効または期限切れです。","en":"Code invalid or expired.","zh-Hant":"驗證碼無效或已過期。","zh-Hans":"验证码无效或已过期。"},
    "err_email_used": {"ja":"このメールは既に使用されています。","en":"Email already in use.","zh-Hant":"此 Email 已被使用。","zh-Hans":"该 Email 已被使用。"},
    # 頁面標語／品牌
    "brand": {
        "ja": "旅行管理", "en": "Travel Manager",
        "zh-Hant": "旅行管理", "zh-Hans": "旅行管理",
    },
    "login_subtitle": {
        "ja": "旅の計画を、シンプルに。",
        "en": "Plan your trips, simply.",
        "zh-Hant": "讓旅程規劃更簡單。",
        "zh-Hans": "让行程规划更简单。",
    },
    "register_subtitle": {
        "ja": "旅の計画、荷物、日程を一括管理。",
        "en": "Manage plans, packing and itinerary in one place.",
        "zh-Hant": "集中管理計畫、行李與行程。",
        "zh-Hans": "集中管理计划、行李与行程。",
    },

    # 寄驗證碼流程（上半部）
    "email_verification": {
        "ja":"メール認証", "en":"Email verification",
        "zh-Hant":"郵件驗證", "zh-Hans":"邮件验证",
    },
    "sending": {
        "ja":"送信中…", "en":"Sending…",
        "zh-Hant":"傳送中…", "zh-Hans":"发送中…",
    },
    "resend_in": {
        "ja":"再送まで", "en":"Resend in",
        "zh-Hant":"可再次寄送於", "zh-Hans":"可再次发送于",
    },
    "send_failed": {
        "ja":"送信に失敗しました。後でもう一度お試しください。",
        "en":"Failed to send. Please try again later.",
        "zh-Hant":"寄送失敗，請稍後再試。",
        "zh-Hans":"发送失败，请稍后再试。",
    },
    "register_hint": {
        "ja":"メールで届いた6桁コードを入力して登録を完了してください。",
        "en":"Enter the 6-digit code from the email to complete sign up.",
        "zh-Hant":"請輸入 Email 的 6 位驗證碼完成註冊。",
        "zh-Hans":"请输入 Email 的 6 位验证码完成注册。",
    },
})
