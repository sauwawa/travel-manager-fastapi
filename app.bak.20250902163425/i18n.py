from typing import Dict

LANGS = {"ja", "en", "zh-Hant", "zh-Hans"}

STRINGS: Dict[str, Dict[str, str]] = {
    # 應用名稱與導覽
    "app_title": {"ja":"旅行管理","en":"Travel Manager","zh-Hant":"旅行管理","zh-Hans":"旅行管理"},
    "owner_app_fmt": {  # 會把 {name} 與 {app} 代入
        "ja": "{name}の{app}",
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
    "sort_hint": {
        "ja":"✔ 旅行/項目をドラッグして並べ替えできます。離すと自動保存されます。",
        "en":"✔ Drag trips/items to reorder. Changes save automatically.",
        "zh-Hant":"✔ 旅行/項目可拖曳調整順序，放開即自動儲存。",
        "zh-Hans":"✔ 旅行/项目可拖拽调整顺序，放开即自动保存。",
    },

    # 欄位（label 與 placeholder 分離）
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

    # 空狀態/刪除確認
    "no_trips":{"ja":"まだ旅行がありません。右上の「新規作成」から追加してください。","en":"No trips yet. Click “New” to add one.","zh-Hant":"尚未有旅行，請點右上「新增」。","zh-Hans":"尚未有旅行，请点右上“新增”。"},
    "no_items":{"ja":"まだ項目がありません。","en":"No items yet.","zh-Hant":"尚未有項目。","zh-Hans":"尚未有项目。"},
    "delete_trip":{"ja":"旅行を削除","en":"Delete Trip","zh-Hant":"刪除旅行","zh-Hans":"删除旅行"},
    "delete_trip_confirm":{"ja":"この旅行とすべての項目を削除しますか？","en":"Delete this trip and all items?","zh-Hant":"要刪除整個旅行與所有項目嗎？","zh-Hans":"要删除整个旅行与所有项目吗？"},
    "delete_item_confirm":{"ja":"この項目を削除しますか？","en":"Delete this item?","zh-Hant":"要刪除這個項目嗎？","zh-Hans":"要删除这个项目吗？"},

    # 語言選單
    "lang_ja":{"ja":"日本語","en":"Japanese","zh-Hant":"日文","zh-Hans":"日文"},
    "lang_en":{"ja":"英語","en":"English","zh-Hant":"英文","zh-Hans":"英文"},
    "lang_zh_hant":{"ja":"繁體字","en":"Chinese (Traditional)","zh-Hant":"繁體中文","zh-Hans":"繁体中文"},
    "lang_zh_hans":{"ja":"簡体字","en":"Chinese (Simplified)","zh-Hant":"簡體中文","zh-Hans":"简体中文"},

    # 認證
    "login":{"ja":"ログイン","en":"Login","zh-Hant":"登入","zh-Hans":"登录"},
    "logout":{"ja":"ログアウト","en":"Logout","zh-Hant":"登出","zh-Hans":"退出"},
    "register":{"ja":"新規登録","en":"Sign up","zh-Hant":"註冊","zh-Hans":"注册"},
    "login_title":{"ja":"ログイン","en":"Login","zh-Hant":"登入","zh-Hans":"登录"},
    "register_title":{"ja":"新規登録","en":"Sign up","zh-Hant":"註冊","zh-Hans":"注册"},
    "login_id":{"ja":"ID（ログインID）","en":"ID (login)","zh-Hant":"登入ID","zh-Hans":"登录ID"},
    "password":{"ja":"パスワード","en":"Password","zh-Hant":"密碼","zh-Hans":"密码"},
    "username_label":{"ja":"User name（表示名）","en":"User name (display)","zh-Hant":"使用者名稱","zh-Hans":"用户名"},
    "email":{"ja":"Email","en":"Email","zh-Hant":"Email","zh-Hans":"Email"},
    "email_confirm":{"ja":"Email（確認）","en":"Email (confirm)","zh-Hant":"Email（確認）","zh-Hans":"Email（确认）"},
    "register_submit":{"ja":"登録","en":"Sign up","zh-Hant":"註冊","zh-Hans":"注册"},
    "go_login":{"ja":"ログインへ","en":"Go to login","zh-Hant":"前往登入","zh-Hans":"前往登录"},
    "go_register":{"ja":"新規登録","en":"Sign up","zh-Hant":"註冊","zh-Hans":"注册"},

    # 錯誤訊息
    "error_email_mismatch":{"ja":"Emailと確認が一致しません。","en":"Email and confirmation do not match.","zh-Hant":"Email 與確認不一致。","zh-Hans":"Email 与确认不一致。"},
    "error_id_or_email_used":{"ja":"IDまたはEmailは既に使用されています。","en":"Login ID or Email is already in use.","zh-Hant":"登入ID 或 Email 已被使用。","zh-Hans":"登录ID 或 Email 已被使用。"},
    "error_login_bad":{"ja":"IDまたはパスワードが違います。","en":"Invalid ID or password.","zh-Hant":"ID 或密碼錯誤。","zh-Hans":"ID 或密码错误。"},
}

def get_lang(request) -> str:
    code = request.cookies.get("lang", "ja")
    return code if code in LANGS else "ja"

def get_L(lang: str):
    return {k: (v.get(lang) or v.get("ja") or k) for k, v in STRINGS.items()}
