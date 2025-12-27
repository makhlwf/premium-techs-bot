import os
import telebot
from telebot.handler_backends import State, StatesGroup
from telebot import custom_filters
from telebot.util import quick_markup
from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove,
)
from dotenv import load_dotenv
from deep_translator import GoogleTranslator
import requests
from bs4 import BeautifulSoup
import io
from google_play_scraper import app as play_scraper
from urllib.parse import parse_qs, urlparse

load_dotenv(override=True)

# --- Translation System ---
translations = {
    "ar": {
        "welcome": "👋 أهلاً بك في بوت النشر الخاص بـ Premium Techs.\n🤖 يساعدك هذا البوت في نشر التطبيقات على قنواتنا.\n📝 **الخطوات:**\n1. اختر نوع المنشور\n2. أدخل اسم التطبيق وإصداره\n3. أدخل الوصف (مترجم تلقائياً)\n4. اختر ميزات التعديل (اختيار متعدد)\n5. ارفع الأيقونة والملف.\n⚠️ **ملاحظة:** تتم مراجعة جميع المنشورات من قبل المسؤولين قبل النشر.",
        "start_button": "ابدأ",
        "unauthorized": "! أنت غير مصرح لك باستخدام هذا البوت.",
        "post_type_question": "يرجى اختيار نوع المنشور:",
        "app_button": "تطبيق",
        "game_button": "لعبة",
        "app_type_question": "يرجى اختيار نوع التطبيق:",
        "mod_button": "معدل",
        "official_button": "رسمي",
        "great_next_step": "عظيم! لننتقل إلى الخطوة التالية.",
        "source_question": "هل هذا من مقترحات القناة أم من طلبات المشتركين؟",
        "channel_recommendation": "من مقترحات القناة",
        "subscriber_request": "من طلبات المشتركين",
        "got_it": "فهمت!",
        "publish_target_question": "أين تريد النشر؟",
        "arabic_button": "العربية",
        "english_button": "الإنجليزية",
        "both_button": "كلاهما",
        "awesome": "رائع!",
        "app_name_question": "الرجاء إدخال اسم التطبيق.",
        "app_version_question": "الرجاء إدخال إصدار التطبيق.",
        "app_description_question": "الرجاء إدخال وصف التطبيق (باللغة العربية).",
        "translate_question": "هل تريد تقديم ترجمة باللغة الإنجليزية يدوياً أم ترجمتها تلقائياً؟",
        "manual_button": "يدوياً",
        "auto_button": "تلقائياً",
        "manual_translation_prompt": "الرجاء إدخال الترجمة باللغة الإنجليزية للوصف (باللغة الإنجليزية).",
        "auto_translation_used": "سيتم استخدام الترجمة التلقائية.",
        "mod_features_question": "الرجاء اختيار ميزات التعديل من القائمة أو كتابة ميزة تعديل من عندك :",
        "app_image_question": "الرجاء إرسال صورة التطبيق.",
        "app_image_question_with_url": "الرجاء إرسال صورة التطبيق أو رابط التطبيق على متجر جوجل بلاي.",
        "fetch_error": "الرابط غير صالح أو تعذر استخراج الصورة، الرجاء إرسال الصورة يدوياً.",
        "hashtag_question": "الرجاء اختيار هاشتاج للتطبيق او اكتب هاشتاج من عندك :",
        "app_file_question": "الرجاء رفع ملفات التطبيق. يمكنك إرسال أكثر من ملف (بحد أقصى 10). ويجب ان تكون الملفات قد تم إعادة تسميتها والحاق @premium_techs في نهاية الملف وأن قد تم تغيير الصورة المصغرة للملف, يمكنك السؤال في المجتمع عن التفاصيل. عند الانتهاء اضغط على '✅ تم'.",
        "file_received": "✅ تم استلام الملف {count}. أرسل الملف التالي أو اضغط '✅ تم'.",
        "file_limit_reached": "⚠️ لقد وصلت إلى الحد الأقصى للملفات (10). اضغط '✅ تم' للمتابعة.",
        "file_missing_warning": "⚠️ الرجاء إرسال ملف واحد على الأقل.",
        "done_button": "✅ تم",
        "review_prompt": "الرجاء مراجعة المعلومات التي قدمتها:",
        "confirm_button": "تأكيد",
        "restart_button": "إعادة البدء",
        "request_submitted": "تم إرسال طلبك للمراجعة.",
        "request_pending": "تم إرسال طلبك وهو قيد المراجعة.",
        "restarting": "إعادة التشغيل...",
        "new_submission": "لديك طلب نشر جديد من",
        "approve_button": "موافقة",
        "reject_button": "رفض",
        "post_approved": "تمت الموافقة على طلب النشر الخاص بك.",
        "post_rejected": "تم رفض طلب النشر الخاص بك.",
        "poll_question": "ما هو تقييمك للتطبيق؟",
        "poll_options": ["🔥 ممتاز", "⚡️ جيد", "😐 عادي", "👎 سيء"],
        "ask_rejection_reason": "الرجاء كتابة سبب الرفض.",
        "rejection_sent": "تم إرسال الرفض للمستخدم.",
        "rejection_notification": "تم رفض طلبك. السبب: ",
        "cancel_button": "إلغاء",
        "rejection_cancelled": "تم إلغاء الرفض.",
        "error_missing_data_msg_update": "تم إخطار المستخدم، ولكن تعذر تحديث رسالة الطلب الأصلية (البيانات مفقودة).",
        "back_button": "🔙 رجوع",
        "btn_auto_fill": "⚡️ تعبئة تلقائية",
        "btn_approve": "✅ اعتماد",
        "btn_reject": "❌ إلغاء",
        "btn_edit_name": "✏️ تعديل الاسم",
        "btn_edit_desc": "✏️ تعديل الوصف",
        "btn_edit_image": "✏️ تعديل الصورة",
        "btn_deep_fetch": "📜 جلب عميق",
        "ask_autofill": "الرجاء إرسال **اسم التطبيق** للبحث عنه، أو **رابط** التطبيق على متجر جوجل بلاي.",
        "preview_caption": "🔍 نتيجة البحث:\n\n📌 الاسم: {name}\n📝 الوصف: {desc}...\n\nهل تريد اعتماد هذه البيانات؟",
        "error_not_found": "❌ لم يتم العثور على التطبيق. الرجاء المحاولة مرة أخرى أو إرسال الرابط مباشرة.",
    },
    "en": {
        "poll_question": "Rate this app",
        "poll_options": ["🔥 Excellent", "⚡️ Good", "😐 Normal", "👎 Bad"],
        "ask_rejection_reason": "Please enter the rejection reason.",
        "rejection_sent": "Rejection reason sent to user.",
        "rejection_notification": "Your request was rejected. Reason: ",
        "cancel_button": "Cancel",
        "rejection_cancelled": "Rejection cancelled.",
        "error_missing_data_msg_update": "User notified, but could not update original request message (Data missing).",
    },
}


def get_text(key, lang="ar"):
    return translations[lang][key]


def smart_truncate(text, limit=550):
    if not text:
        return ""
    if len(text) <= limit:
        return text
    return text[:limit].rstrip().rsplit(" ", 1)[0] + "..."


def get_back_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton(get_text("back_button")))
    return markup


def get_done_markup():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(get_text("done_button"), callback_data="files_done"),
        InlineKeyboardButton(get_text("back_button"), callback_data="go_back"),
    )
    return markup


def get_features_markup(selected_set):
    markup = InlineKeyboardMarkup(row_width=2)
    standard_tags = [
        "Premium",
        "مهكر",
        "بدون إعلانات",
        "Pro",
        "مدفوع",
        "Mod",
        "يجب تشغيل VPN",
        "يحوي بعض المشكلات",
        "تم اختراق السيرفر",
        "تحديث جديد",
        "تمت اضافة ترجمة",
    ]

    buttons = []
    for tag in standard_tags:
        text = f"✅ {tag}" if tag in selected_set else tag
        buttons.append(InlineKeyboardButton(text, callback_data=f"feat_{tag}"))

    markup.add(*buttons)
    markup.add(InlineKeyboardButton("✅ تم (Done)", callback_data="feat_done"))
    markup.add(InlineKeyboardButton("🔙 رجوع", callback_data="go_back"))
    return markup


def fetch_icon_from_play_store(url):
    """
    Fetches the app icon URL from a Google Play Store page.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.content, "html.parser")

        # Try finding the icon using itemprop="image"
        icon_tag = soup.find("img", {"itemprop": "image"})

        if not icon_tag:
            # Try class T75of which is common for Play Store icons
            icon_tag = soup.find("img", class_="T75of")

        if not icon_tag:
            return None

        icon_url = icon_tag.get("src")
        if icon_url and icon_url.startswith("//"):
            icon_url = "https:" + icon_url

        return icon_url

    except Exception as e:
        print(f"Error fetching icon: {e}")
        return None


# --- End Translation System ---

# In-memory storage for user data
user_data = {}


class BotStates(StatesGroup):
    start = State()
    post_type = State()
    app_type = State()
    source = State()
    publish_target = State()
    app_name = State()
    waiting_for_autofill = State()
    app_version = State()
    app_description = State()
    translate_description = State()
    manual_translation = State()
    mod_features = State()
    english_mod_features = State()
    app_image = State()
    hashtag = State()
    app_file = State()
    confirmation = State()
    af_edit_name = State()
    af_edit_desc = State()
    af_edit_image = State()
    admin_approval = State()
    admin_rejection_reason = State()


# Initialize the bot with threaded=False for Vercel/webhooks
bot = telebot.TeleBot(
    os.environ.get("BOT_TOKEN"), threaded=False, use_class_middlewares=True
)
bot.add_custom_filter(custom_filters.StateFilter(bot))

# --- Ask Functions ---


def ask_post_type(chat_id, user_id, message_id=None):
    bot.set_state(user_id, BotStates.post_type, chat_id)
    markup = quick_markup(
        {
            get_text("app_button"): {"callback_data": "post_type_app"},
            get_text("game_button"): {"callback_data": "post_type_game"},
        },
        row_width=2,
    )
    # No back button for the first step
    if message_id:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=get_text("post_type_question"),
            reply_markup=markup,
        )
    else:
        bot.send_message(chat_id, get_text("post_type_question"), reply_markup=markup)


def ask_app_type(chat_id, user_id, message_id=None):
    bot.set_state(user_id, BotStates.app_type, chat_id)
    markup = quick_markup(
        {
            get_text("mod_button"): {"callback_data": "app_type_mod"},
            get_text("official_button"): {"callback_data": "app_type_official"},
            get_text("back_button"): {"callback_data": "go_back"},
        },
        row_width=2,
    )
    if message_id:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=get_text("app_type_question"),
            reply_markup=markup,
        )
    else:
        bot.send_message(chat_id, get_text("app_type_question"), reply_markup=markup)


def ask_source(chat_id, user_id, message_id=None):
    bot.set_state(user_id, BotStates.source, chat_id)
    markup = quick_markup(
        {
            get_text("channel_recommendation"): {
                "callback_data": "source_recommendation"
            },
            get_text("subscriber_request"): {"callback_data": "source_request"},
            get_text("back_button"): {"callback_data": "go_back"},
        },
        row_width=2,
    )
    if message_id:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=get_text("source_question"),
            reply_markup=markup,
        )
    else:
        bot.send_message(chat_id, get_text("source_question"), reply_markup=markup)


def ask_publish_target(chat_id, user_id, message_id=None):
    bot.set_state(user_id, BotStates.publish_target, chat_id)
    markup = quick_markup(
        {
            get_text("arabic_button"): {"callback_data": "publish_arabic"},
            get_text("english_button"): {"callback_data": "publish_english"},
            get_text("both_button"): {"callback_data": "publish_both"},
            get_text("back_button"): {"callback_data": "go_back"},
        },
        row_width=3,
    )
    if message_id:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=get_text("publish_target_question"),
            reply_markup=markup,
        )
    else:
        bot.send_message(
            chat_id, get_text("publish_target_question"), reply_markup=markup
        )


def ask_app_name(chat_id, user_id):
    bot.set_state(user_id, BotStates.app_name, chat_id)
    bot.send_message(
        chat_id, get_text("app_name_question"), reply_markup=get_back_markup()
    )

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            get_text("btn_auto_fill"), callback_data="trigger_auto_fill"
        )
    )
    bot.send_message(chat_id, "👇", reply_markup=markup)


def send_autofill_preview(chat_id, user_id, message_id_to_delete=None):
    if message_id_to_delete:
        try:
            bot.delete_message(chat_id, message_id_to_delete)
        except Exception:
            pass

    temp = user_data[user_id].get("temp_autofill")
    if not temp:
        bot.send_message(chat_id, get_text("error_not_found"))
        ask_app_name(chat_id, user_id)
        return

    # Use translated_ar_desc for the preview
    app_desc = temp["translated_ar_desc"]
    short_desc = (app_desc[:600] + "...") if len(app_desc) > 600 else app_desc
    caption = get_text("preview_caption").format(name=temp["name"], desc=short_desc)

    markup = InlineKeyboardMarkup(row_width=2)
    # Row 1: Edit buttons
    markup.row(
        InlineKeyboardButton(get_text("btn_edit_name"), callback_data="af_edit_name"),
        InlineKeyboardButton(get_text("btn_edit_desc"), callback_data="af_edit_desc"),
    )
    markup.row(
        InlineKeyboardButton(get_text("btn_edit_image"), callback_data="af_edit_image"),
        InlineKeyboardButton(get_text("btn_deep_fetch"), callback_data="af_deep_fetch"),
    )

    # Row 2: Approve/Reject
    markup.row(
        InlineKeyboardButton(get_text("btn_approve"), callback_data="af_approve"),
        InlineKeyboardButton(get_text("btn_reject"), callback_data="af_reject"),
    )

    try:
        # Check if icon is a URL or file_id
        if temp["icon"].startswith("http"):
            bot.send_photo(chat_id, temp["icon"], caption=caption, reply_markup=markup)
        else:
            bot.send_photo(chat_id, temp["icon"], caption=caption, reply_markup=markup)
    except Exception as e:
        print(f"Error sending preview: {e}")
        bot.send_message(chat_id, get_text("error_not_found"))


@bot.callback_query_handler(
    func=lambda call: call.data in ["af_edit_name", "af_edit_desc", "af_edit_image"]
)
def autofill_edit_callback(call):
    user_id = call.from_user.id
    action = call.data

    # Store the message ID to delete it later or update it
    # Ideally we just send a new prompt and let the user reply.
    # The prompt should be text.

    if action == "af_edit_name":
        bot.set_state(user_id, BotStates.af_edit_name, call.message.chat.id)
        bot.send_message(call.message.chat.id, "الرجاء إرسال الاسم الجديد:")

    elif action == "af_edit_desc":
        bot.set_state(user_id, BotStates.af_edit_desc, call.message.chat.id)
        bot.send_message(
            call.message.chat.id, "الرجاء إرسال الوصف الجديد (باللغة العربية):"
        )

    elif action == "af_edit_image":
        bot.set_state(user_id, BotStates.af_edit_image, call.message.chat.id)
        bot.send_message(call.message.chat.id, "الرجاء إرسال الصورة الجديدة (صورة):")

    bot.answer_callback_query(call.id)
    # We don't delete the preview message here, so the user can see context,
    # but the new preview will appear below after input.


def escape_markdown(text):
    """Escapes Markdown special characters to prevent API errors."""
    if not text:
        return ""
    # Escape chars that are special in legacy Markdown: * _ ` [ ] ( )
    # Note: Legacy Markdown is less strict but * and _ are crucial.
    chars = ["*", "_", "`", "[", "]"]
    for c in chars:
        text = text.replace(c, "\\" + c)
    return text


@bot.callback_query_handler(func=lambda call: call.data == "af_deep_fetch")
def autofill_deep_fetch_callback(call):
    user_id = call.from_user.id
    temp = user_data[user_id].get("temp_autofill")
    if not temp:
        bot.answer_callback_query(call.id, "No data")
        return

    summary = escape_markdown(temp.get("translated_summary", ""))
    desc = escape_markdown(temp.get("translated_deep_desc", ""))
    changes = escape_markdown(temp.get("translated_changes", ""))

    # Construct the deep fetch message
    msg_text = (
        f"📦 **نتيجة الجلب العميق:**\n\n"
        f"🔹 **الملخص:**\n{summary}\n\n"
        f"🔹 **الوصف:**\n{desc}\n\n"
        f"🔹 **التغييرات:**\n{changes}"
    )

    # Send, splitting if necessary (simple approach: just send, telegram splits up to 4096)
    # If > 4096, we might need manual split, but let's try sending first.
    # Python strings are utf-8.

    # Safe splitting (by newline if possible) to avoid breaking Markdown
    if len(msg_text) > 4000:
        # Split by sections first if possible, or just plain text splitting at newlines
        parts = []
        while len(msg_text) > 0:
            if len(msg_text) <= 4000:
                parts.append(msg_text)
                break

            # Find nearest newline before limit
            limit = 4000
            split_idx = msg_text.rfind("\n", 0, limit)
            if split_idx == -1:
                # No newline found, force split (rare case)
                split_idx = limit

            parts.append(msg_text[:split_idx])
            msg_text = msg_text[
                split_idx:
            ].lstrip()  # Remove leading newline in next part

        for part in parts:
            if part.strip():
                bot.send_message(call.message.chat.id, part, parse_mode="Markdown")
    else:
        bot.send_message(call.message.chat.id, msg_text, parse_mode="Markdown")

    bot.answer_callback_query(call.id)


@bot.message_handler(state=BotStates.af_edit_name)
def af_edit_name_handler(message):
    user_id = message.from_user.id
    new_name = message.text
    if user_data[user_id].get("temp_autofill"):
        user_data[user_id]["temp_autofill"]["name"] = new_name

    send_autofill_preview(message.chat.id, user_id)


@bot.message_handler(state=BotStates.af_edit_desc)
def af_edit_desc_handler(message):
    user_id = message.from_user.id
    new_desc = message.text
    if user_data[user_id].get("temp_autofill"):
        user_data[user_id]["temp_autofill"]["translated_ar_desc"] = new_desc
        user_data[user_id]["temp_autofill"]["is_desc_edited"] = True

    send_autofill_preview(message.chat.id, user_id)


@bot.message_handler(state=BotStates.af_edit_image, content_types=["photo"])
def af_edit_image_handler(message):
    user_id = message.from_user.id

    file_id = message.photo[-1].file_id
    if user_data[user_id].get("temp_autofill"):
        user_data[user_id]["temp_autofill"]["icon"] = file_id
    send_autofill_preview(message.chat.id, user_id)


def ask_app_version(chat_id, user_id):
    bot.set_state(user_id, BotStates.app_version, chat_id)
    bot.send_message(
        chat_id, get_text("app_version_question"), reply_markup=get_back_markup()
    )


def ask_app_description(chat_id, user_id):
    if user_data.get(user_id, {}).get("auto_filled"):
        ask_mod_features(chat_id, user_id)
        return

    bot.set_state(user_id, BotStates.app_description, chat_id)
    bot.send_message(
        chat_id, get_text("app_description_question"), reply_markup=get_back_markup()
    )


def ask_translate_description(chat_id, user_id, message_id=None):
    bot.set_state(user_id, BotStates.translate_description, chat_id)
    markup = quick_markup(
        {
            get_text("manual_button"): {"callback_data": "translate_manual"},
            get_text("auto_button"): {"callback_data": "translate_auto"},
            get_text("back_button"): {"callback_data": "go_back"},
        },
        row_width=2,
    )
    if message_id:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=get_text("translate_question"),
            reply_markup=markup,
        )
    else:
        bot.send_message(chat_id, get_text("translate_question"), reply_markup=markup)


def ask_manual_translation(chat_id, user_id):
    bot.set_state(user_id, BotStates.manual_translation, chat_id)
    bot.send_message(
        chat_id, get_text("manual_translation_prompt"), reply_markup=get_back_markup()
    )


def ask_mod_features(chat_id, user_id, message_id=None):
    bot.set_state(user_id, BotStates.mod_features, chat_id)

    if "selected_features" not in user_data[user_id]:
        user_data[user_id]["selected_features"] = set()

    markup = get_features_markup(user_data[user_id]["selected_features"])

    if message_id:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=get_text("mod_features_question"),
            reply_markup=markup,
        )
    else:
        bot.send_message(
            chat_id, get_text("mod_features_question"), reply_markup=markup
        )


def ask_english_mod_features(chat_id, user_id):
    bot.set_state(user_id, BotStates.english_mod_features, chat_id)
    bot.send_message(
        chat_id,
        "الرجاء إدخال ميزات التعديل باللغة الإنجليزية.",
        reply_markup=get_back_markup(),
    )


def ask_app_image(chat_id, user_id):
    is_autofilled = user_data.get(user_id, {}).get("auto_filled", False)
    has_image = "app_image" in user_data.get(user_id, {})

    if is_autofilled and has_image:
        ask_app_file(chat_id, user_id)
        return

    bot.set_state(user_id, BotStates.app_image, chat_id)
    bot.send_message(
        chat_id, get_text("app_image_question_with_url"), reply_markup=get_back_markup()
    )


def ask_hashtag(chat_id, user_id, message_id=None):
    if user_data[user_id].get("post_type") == "game":
        # Skip hashtag selection for games
        user_data[user_id]["hashtag"] = "#games"
        ask_app_image(chat_id, user_id)
        return

    bot.set_state(user_id, BotStates.hashtag, chat_id)
    hashtags = {
        "تواصل اجتماعي": {"callback_data": "#Social"},
        "تعديل": {"callback_data": "#editing"},
        "VPN": {"callback_data": "#vpn"},
        "أدوات": {"callback_data": "#Tools"},
        "مشاهدة": {"callback_data": "#watching"},
        "وسائط متعددة": {"callback_data": "#multimedia"},
        "متصفح": {"callback_data": "#browser"},
        "ترجمة": {"callback_data": "#translate"},
        "متجر": {"callback_data": "#store"},
        "تسجيل": {"callback_data": "#record"},
        "نصائح": {"callback_data": "#tips"},
        "كتب": {"callback_data": "#books"},
        "خلفيات": {"callback_data": "#wallpapers"},
        "ثيمات": {"callback_data": "#themes"},
        "تعليم": {"callback_data": "#learning"},
        "ديني": {"callback_data": "#religious"},
        "أخبار": {"callback_data": "#news"},
        "موسيقى": {"callback_data": "#music"},
        "كيبورد": {"callback_data": "#keyboard"},
        "كاميرا": {"callback_data": "#camera"},
        "ذكاء اصطناعي": {"callback_data": "#AI"},
        get_text("back_button"): {"callback_data": "go_back"},
    }
    markup = quick_markup(hashtags, row_width=3)
    if message_id:
        pass

    bot.send_message(chat_id, get_text("hashtag_question"), reply_markup=markup)


def ask_app_file(chat_id, user_id):
    bot.set_state(user_id, BotStates.app_file, chat_id)
    # Clear previous Reply Keyboard
    msg = bot.send_message(
        chat_id,
        "🔄 جاري تحضير قائمة الملفات...",
        reply_markup=ReplyKeyboardRemove(),
    )
    bot.delete_message(chat_id, msg.message_id)

    bot.send_message(
        chat_id, get_text("app_file_question"), reply_markup=get_done_markup()
    )


def ask_confirmation(chat_id, user_id):
    bot.set_state(user_id, BotStates.confirmation, chat_id)
    data = user_data[user_id]
    # Truncate descriptions for preview to prevent caption overflow
    preview_desc_ar = smart_truncate(data.get("app_description", ""), limit=300)

    confirmation_message = f"""{get_text("review_prompt")}

نوع التطبيق: {data.get("app_type")}
المصدر: {data.get("source")}
وجهة النشر: {data.get("publish_target")}
اسم التطبيق: {data.get("app_name")}
إصدار التطبيق: {data.get("app_version")}
وصف التطبيق: {preview_desc_ar}
الهاشتاج: {data.get("hashtag")}
"""
    if "english_description" in data:
        preview_desc_en = smart_truncate(data.get("english_description", ""), limit=300)
        confirmation_message += f"الوصف باللغة الإنجليزية: {preview_desc_en}\n"
    if "mod_features" in data:
        confirmation_message += f"ميزات التعديل: {data.get('mod_features')}\n"
    if "english_mod_features" in data:
        confirmation_message += (
            f"ميزات التعديل باللغة الإنجليزية: {data.get('english_mod_features')}\n"
        )

    markup = quick_markup(
        {
            get_text("confirm_button"): {"callback_data": "confirm"},
            get_text("restart_button"): {"callback_data": "restart"},
            get_text("back_button"): {"callback_data": "go_back"},
        },
        row_width=2,
    )
    bot.send_photo(
        chat_id=chat_id,
        photo=data["app_image"],
        caption=confirmation_message,
        reply_markup=markup,
    )

    # Send files to user for verification
    files = data.get("app_files", [])
    if not files and "app_file" in data:
        files = [data["app_file"]]

    for file_id in files:
        bot.send_document(chat_id=chat_id, document=file_id)


# --- Handlers ---


@bot.message_handler(commands=["start"])
def start_command(message):
    # This version cleans up spaces and empty lines automatically
    allowed_raw = os.environ.get("ALLOWED_POSTERS_IDS", "")
    allowed_posters_ids = [i.strip() for i in allowed_raw.split(",") if i.strip()]
    
    admin_raw = os.environ.get("FULL_ADMIN_ID", "")
    full_admin_ids = [i.strip() for i in admin_raw.split(",") if i.strip()]

    user_id_str = str(message.from_user.id)
    
    # Check if the user is in either list
    if user_id_str not in allowed_posters_ids and user_id_str not in full_admin_ids:
        bot.send_message(message.chat.id, get_text("unauthorized"))
        return

    markup = quick_markup(
        {get_text("start_button"): {"callback_data": "start_conversation"}}
    )
    bot.send_message(
        message.chat.id, get_text("welcome"), reply_markup=markup, parse_mode="Markdown"
    )


@bot.callback_query_handler(func=lambda call: call.data == "start_conversation")
def start_conversation_callback(call):
    ask_post_type(call.message.chat.id, call.from_user.id, call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("post_type_"))
def post_type_callback(call):
    user_id = call.from_user.id
    user_data[user_id] = {
        "post_type": call.data.split("_")[2],
        "original_poster_id": user_id,
    }
    bot.answer_callback_query(call.id, f"لقد اخترت: {user_data[user_id]['post_type']}")
    ask_app_type(call.message.chat.id, user_id, call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("app_type_"))
def app_type_callback(call):
    user_id = call.from_user.id
    user_data[user_id]["app_type"] = call.data.split("_")[2]
    bot.answer_callback_query(call.id, f"لقد اخترت: {user_data[user_id]['app_type']}")
    ask_source(call.message.chat.id, user_id, call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("source_"))
def source_callback(call):
    user_id = call.from_user.id
    user_data[user_id]["source"] = call.data.split("_")[1]
    bot.answer_callback_query(call.id, f"لقد اخترت: {user_data[user_id]['source']}")
    ask_publish_target(call.message.chat.id, user_id, call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("publish_"))
def publish_target_callback(call):
    user_id = call.from_user.id
    user_data[user_id]["publish_target"] = call.data.split("_")[1]
    bot.answer_callback_query(
        call.id, f"لقد اخترت: {user_data[user_id]['publish_target']}"
    )
    ask_app_name(call.message.chat.id, user_id)


@bot.callback_query_handler(func=lambda call: call.data == "trigger_auto_fill")
def trigger_auto_fill_callback(call):
    user_id = call.from_user.id
    bot.set_state(user_id, BotStates.waiting_for_autofill, call.message.chat.id)
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id, get_text("ask_autofill"), reply_markup=get_back_markup()
    )


@bot.message_handler(state=BotStates.waiting_for_autofill)
def autofill_input_handler(message):
    user_id = message.from_user.id
    if message.text == get_text("back_button"):
        go_back(message.chat.id, user_id)
        return

    text = message.text
    target_url = None

    msg = bot.send_message(message.chat.id, "⏳ جارٍ البحث...")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    if "play.google.com" in text:
        target_url = text
        if "hl=" not in target_url:
            target_url += "&hl=en&gl=us"
        elif "hl=ar" in target_url:
            target_url = target_url.replace("hl=ar", "hl=en")
            if "gl=" not in target_url:
                target_url += "&gl=us"
    else:
        # Search in English store using BS4 (Hybrid Approach)
        search_url = f"https://play.google.com/store/search?q={text}&c=apps&hl=en&gl=us"
        try:
            resp = requests.get(search_url, headers=headers)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.content, "html.parser")
                for a in soup.find_all("a", href=True):
                    href = a["href"]
                    if "/store/apps/details?id=" in href:
                        target_url = "https://play.google.com" + href
                        if "&hl=en" not in target_url:
                            target_url += "&hl=en&gl=us"
                        break
        except Exception as e:
            print(f"Search error: {e}")

    if not target_url:
        bot.delete_message(message.chat.id, msg.message_id)
        bot.send_message(message.chat.id, get_text("error_not_found"))
        return

    try:
        # Extract ID
        parsed = urlparse(target_url)
        params = parse_qs(parsed.query)
        app_id = params.get("id", [None])[0]

        if not app_id:
            bot.delete_message(message.chat.id, msg.message_id)
            bot.send_message(message.chat.id, get_text("error_not_found"))
            return

        # Fetch details using play_scraper
        result = play_scraper(app_id, lang="en", country="us")

        app_name = result.get("title", text)
        desc_en = result.get("description", "")
        summary_en = result.get("summary", "")
        changes_en = result.get("recentChanges", "") or ""  # Might be None

        # Prepare Text
        truncated_en_preview = (
            (desc_en[:1200] + "...") if len(desc_en) > 1200 else desc_en
        )
        truncated_en_deep = (desc_en[:3000] + "...") if len(desc_en) > 3000 else desc_en

        # Translate
        translator = GoogleTranslator(source="en", target="ar")

        # 1. Preview Desc
        try:
            translated_ar = translator.translate(truncated_en_preview)
        except Exception as e:
            print(f"Translation error (preview): {e}")
            translated_ar = truncated_en_preview

        final_ar_preview = (
            (translated_ar[:950] + "...") if len(translated_ar) > 950 else translated_ar
        )

        # 2. Deep Fetch Desc
        try:
            translated_deep = translator.translate(truncated_en_deep)
        except Exception as e:
            print(f"Translation error (deep): {e}")
            translated_deep = truncated_en_deep

        # 3. Summary
        try:
            translated_summary = translator.translate(summary_en) if summary_en else ""
        except Exception:
            translated_summary = summary_en

        # 4. Changes
        try:
            translated_changes = (
                translator.translate(changes_en) if changes_en else "لا يوجد"
            )
        except Exception:
            translated_changes = changes_en

        icon_url = result.get("icon")

        if not icon_url:
            bot.delete_message(message.chat.id, msg.message_id)
            bot.send_message(message.chat.id, get_text("error_not_found"))
            return

        user_data[user_id]["temp_autofill"] = {
            "name": app_name,
            "scraped_en_desc": truncated_en_preview,  # Store truncated preview version
            "translated_ar_desc": final_ar_preview,
            "translated_deep_desc": translated_deep,
            "translated_summary": translated_summary,
            "translated_changes": translated_changes,
            "is_desc_edited": False,
            "icon": icon_url,
            "url": target_url,
        }

        bot.delete_message(message.chat.id, msg.message_id)
        send_autofill_preview(message.chat.id, user_id)

    except Exception as e:
        print(f"Scrape error: {e}")
        bot.delete_message(message.chat.id, msg.message_id)
        bot.send_message(message.chat.id, get_text("error_not_found"))


@bot.callback_query_handler(func=lambda call: call.data in ["af_approve", "af_reject"])
def autofill_callback_handler(call):
    user_id = call.from_user.id
    if call.data == "af_reject":
        bot.answer_callback_query(call.id, "Cancelled")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        ask_app_name(call.message.chat.id, user_id)

    elif call.data == "af_approve":
        temp = user_data[user_id].get("temp_autofill")
        if not temp:
            bot.answer_callback_query(call.id, "Error: Data expired.")
            ask_app_name(call.message.chat.id, user_id)
            return

        bot.answer_callback_query(call.id, "Approved")

        user_data[user_id].update(
            {
                "app_name": temp["name"],
                "app_description": temp["translated_ar_desc"],
                "auto_filled": True,
            }
        )

        # Ensure post_type exists (default to app if missing)
        if "post_type" not in user_data[user_id]:
            user_data[user_id]["post_type"] = "app"

        # Handle Icon
        # If it's a URL, download it. If it's a file_id (edited), use it.
        if temp["icon"].startswith("http"):
            try:
                img_resp = requests.get(temp["icon"])
                if img_resp.status_code == 200:
                    photo_file = io.BytesIO(img_resp.content)
                    photo_file.name = "icon.jpg"

                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    sent_msg = bot.send_photo(
                        call.message.chat.id, photo_file, caption=f"✅ {temp['name']}"
                    )
                    user_data[user_id]["app_image"] = sent_msg.photo[-1].file_id
                else:
                    bot.send_message(
                        call.message.chat.id,
                        "⚠️ Failed to download icon. Please upload it manually later.",
                    )
            except Exception as e:
                print(f"Image download error: {e}")
        else:
            # Already a file_id from user upload
            user_data[user_id]["app_image"] = temp["icon"]
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_photo(
                call.message.chat.id, temp["icon"], caption=f"✅ {temp['name']}"
            )

        # Handle English Description
        publish_target = user_data[user_id].get("publish_target")
        if publish_target in ["english", "both"]:
            if temp.get("is_desc_edited"):
                # Re-translate edited Arabic to English
                try:
                    eng_desc = GoogleTranslator(source="ar", target="en").translate(
                        temp["translated_ar_desc"]
                    )
                    user_data[user_id]["english_description"] = eng_desc
                except Exception as e:
                    print(f"Auto-translate error: {e}")
                    user_data[user_id]["english_description"] = temp[
                        "translated_ar_desc"
                    ]
            else:
                # Use original scraped English
                user_data[user_id]["english_description"] = temp.get("scraped_en_desc")

        ask_app_version(call.message.chat.id, user_id)


@bot.message_handler(state=BotStates.app_name)
def app_name_handler(message):
    user_id = message.from_user.id
    if message.text == get_text("back_button"):
        go_back(message.chat.id, user_id)
        return
    user_data[user_id]["app_name"] = message.text
    ask_app_version(message.chat.id, user_id)


@bot.message_handler(state=BotStates.app_version)
def app_version_handler(message):
    user_id = message.from_user.id
    if message.text == get_text("back_button"):
        go_back(message.chat.id, user_id)
        return
    user_data[user_id]["app_version"] = message.text
    ask_app_description(message.chat.id, user_id)


@bot.message_handler(state=BotStates.app_description)
def app_description_handler(message):
    user_id = message.from_user.id
    if message.text == get_text("back_button"):
        go_back(message.chat.id, user_id)
        return
    user_data[user_id]["app_description"] = message.text
    if user_data[user_id].get("publish_target") in ["english", "both"]:
        ask_translate_description(message.chat.id, user_id)
    else:
        user_data[user_id]["selected_features"] = set()  # Reset features
        ask_mod_features(message.chat.id, user_id)


@bot.callback_query_handler(state=BotStates.translate_description)
def translate_description_callback(call):
    user_id = call.from_user.id
    if call.data == "go_back":
        go_back(call.message.chat.id, user_id)
        return

    if call.data == "translate_manual":
        user_data[user_id]["translation_mode"] = "manual"
        bot.answer_callback_query(call.id, "لقد اخترت: يدوياً")
        ask_manual_translation(call.message.chat.id, user_id)
    elif call.data == "translate_auto":
        user_data[user_id]["translation_mode"] = "auto"
        user_data[user_id]["translate_description"] = "auto"
        bot.answer_callback_query(call.id, "لقد اخترت: تلقائياً")

        # Perform auto translation (Synchronous)
        try:
            translated = GoogleTranslator(source="auto", target="en").translate(
                user_data[user_id]["app_description"]
            )
            user_data[user_id]["english_description"] = translated

            user_data[user_id]["selected_features"] = set()  # Reset features
            ask_mod_features(call.message.chat.id, user_id)
        except Exception as e:
            print(f"Translation error: {e}")
            bot.send_message(
                call.message.chat.id,
                "Automatic translation failed. Please enter the English description manually.",
                reply_markup=get_back_markup(),
            )
            bot.set_state(user_id, BotStates.manual_translation, call.message.chat.id)


@bot.message_handler(state=BotStates.manual_translation)
def manual_translation_handler(message):
    user_id = message.from_user.id
    if message.text == get_text("back_button"):
        go_back(message.chat.id, user_id)
        return
    user_data[user_id]["english_description"] = message.text
    user_data[user_id]["selected_features"] = set()  # Reset features
    ask_mod_features(message.chat.id, user_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("feat_"))
def features_callback_handler(call):
    user_id = call.from_user.id
    action = call.data

    if action == "feat_done":
        selected = user_data[user_id].get("selected_features", set())
        cleaned_list = [f"✓ {f}" for f in selected]
        features_str = "\n".join(sorted(cleaned_list))
        user_data[user_id]["mod_features"] = features_str

        publish_target = user_data[user_id].get("publish_target")
        translation_mode = user_data[user_id].get("translation_mode", "auto")

        if publish_target in ["english", "both"]:
            if translation_mode == "manual":
                ask_english_mod_features(call.message.chat.id, user_id)
            else:
                # Auto translate
                try:
                    translated = GoogleTranslator(source="auto", target="en").translate(
                        features_str
                    )
                    user_data[user_id]["english_mod_features"] = translated
                    ask_hashtag(call.message.chat.id, user_id)
                except Exception as e:
                    print(f"Translation error: {e}")
                    bot.send_message(
                        call.message.chat.id, "Translation failed. Enter manually."
                    )
                    bot.set_state(
                        user_id, BotStates.english_mod_features, call.message.chat.id
                    )
        else:
            ask_hashtag(call.message.chat.id, user_id)
    else:
        tag = action.replace("feat_", "")
        if "selected_features" not in user_data[user_id]:
            user_data[user_id]["selected_features"] = set()

        if tag in user_data[user_id]["selected_features"]:
            user_data[user_id]["selected_features"].remove(tag)
        else:
            user_data[user_id]["selected_features"].add(tag)

        markup = get_features_markup(user_data[user_id]["selected_features"])
        try:
            bot.edit_message_reply_markup(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=markup,
            )
        except Exception:
            pass  # Ignore if identical
        bot.answer_callback_query(call.id)


@bot.message_handler(state=BotStates.mod_features)
def mod_features_handler(message):
    user_id = message.from_user.id
    if message.text == get_text("back_button"):
        go_back(message.chat.id, user_id)
        return

    # Custom Feature
    tag = message.text.replace("✓", "").replace("✅", "").strip()
    if "selected_features" not in user_data[user_id]:
        user_data[user_id]["selected_features"] = set()

    user_data[user_id]["selected_features"].add(tag)

    bot.send_message(message.chat.id, f"✅ تمت إضافة الميزة: {tag}")
    ask_mod_features(message.chat.id, user_id)


@bot.message_handler(state=BotStates.english_mod_features)
def english_mod_features_handler(message):
    user_id = message.from_user.id
    if message.text == get_text("back_button"):
        go_back(message.chat.id, user_id)
        return
    user_data[user_id]["english_mod_features"] = message.text
    ask_hashtag(message.chat.id, user_id)


@bot.message_handler(state=BotStates.app_image, content_types=["photo", "text"])
def app_image_handler(message):
    user_id = message.from_user.id
    if message.content_type == "text" and message.text == get_text("back_button"):
        go_back(message.chat.id, user_id)
        return

    if message.content_type == "photo":
        user_data[user_id]["app_image"] = message.photo[-1].file_id
        ask_app_file(message.chat.id, user_id)

    elif message.content_type == "text":
        url = message.text
        if "play.google.com" in url:
            icon_url = fetch_icon_from_play_store(url)
            if icon_url:
                try:
                    # Download the image
                    img_response = requests.get(icon_url)
                    if img_response.status_code == 200:
                        # Send to chat to get file_id
                        photo_file = io.BytesIO(img_response.content)
                        photo_file.name = "icon.jpg"
                        sent_msg = bot.send_photo(message.chat.id, photo_file)
                        user_data[user_id]["app_image"] = sent_msg.photo[-1].file_id
                        ask_app_file(message.chat.id, user_id)
                    else:
                        bot.send_message(message.chat.id, get_text("fetch_error"))
                except Exception as e:
                    print(f"Error processing image from URL: {e}")
                    bot.send_message(message.chat.id, get_text("fetch_error"))
            else:
                bot.send_message(message.chat.id, get_text("fetch_error"))
        else:
            bot.send_message(message.chat.id, get_text("fetch_error"))


@bot.callback_query_handler(state=BotStates.hashtag)
def hashtag_callback(call):
    user_id = call.from_user.id
    if call.data == "go_back":
        go_back(call.message.chat.id, user_id)
        return

    user_data[user_id]["hashtag"] = call.data
    bot.answer_callback_query(call.id, f"لقد اخترت: {call.data}")
    ask_app_image(call.message.chat.id, user_id)


@bot.message_handler(state=BotStates.hashtag)
def hashtag_text_handler(message):
    user_id = message.from_user.id
    if message.text == get_text("back_button"):
        go_back(message.chat.id, user_id)
        return

    cleaned_text = message.text.replace("#", "").replace(" ", "")
    if not cleaned_text:
        bot.send_message(message.chat.id, "الرجاء إدخال نص صحيح.")
        return

    final_tag = f"#{cleaned_text}"
    user_data[user_id]["hashtag"] = final_tag
    bot.send_message(message.chat.id, f"✅ هاشتاج: {final_tag}")
    ask_app_image(message.chat.id, user_id)


@bot.callback_query_handler(func=lambda call: call.data == "files_done")
def files_done_callback(call):
    user_id = call.from_user.id
    if "app_files" not in user_data[user_id] or not user_data[user_id]["app_files"]:
        bot.answer_callback_query(call.id, get_text("file_missing_warning"))
        bot.send_message(
            call.message.chat.id,
            get_text("file_missing_warning"),
            reply_markup=get_done_markup(),
        )
        return

    bot.answer_callback_query(call.id)
    ask_confirmation(call.message.chat.id, user_id)


@bot.message_handler(state=BotStates.app_file, content_types=["document", "text"])
def app_file_handler(message):
    user_id = message.from_user.id

    # Initialize list if not exists
    if "app_files" not in user_data[user_id]:
        user_data[user_id]["app_files"] = []

    if message.content_type == "document":
        if len(user_data[user_id]["app_files"]) >= 10:
            bot.send_message(
                message.chat.id,
                get_text("file_limit_reached"),
                reply_markup=get_done_markup(),
            )
        else:
            user_data[user_id]["app_files"].append(message.document.file_id)
            count = len(user_data[user_id]["app_files"])
            bot.send_message(
                message.chat.id,
                get_text("file_received").format(count=count),
                reply_markup=get_done_markup(),
            )
    else:
        # If user sends something else (like text)
        bot.send_message(
            message.chat.id,
            get_text("app_file_question"),
            reply_markup=get_done_markup(),
        )


@bot.callback_query_handler(state=BotStates.confirmation)
def confirmation_callback(call):
    user_id = call.from_user.id
    if call.data == "go_back":
        go_back(call.message.chat.id, user_id)
        return

    if call.data == "confirm":
        # Store submitter name for final broadcast
        user_data[user_id]["submitter_name"] = call.from_user.first_name

        bot.answer_callback_query(call.id, get_text("request_submitted"))
        bot.edit_message_caption(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            caption=get_text("request_pending"),
        )

        # Send to full admin for approval
        admin_raw = os.environ.get("FULL_ADMIN_ID", "")
        full_admin_ids = [i.strip() for i in admin_raw.split(",") if i.strip()]
        if full_admin_ids:
            data = user_data[user_id]
            admin_message = f"{get_text('new_submission')} {call.from_user.first_name}:\n\n{call.message.caption}"
            markup = quick_markup(
                {
                    get_text("approve_button"): {
                        "callback_data": f"admin_approve_{user_id}"
                    },
                    get_text("reject_button"): {
                        "callback_data": f"admin_reject_{user_id}"
                    },
                },
                row_width=2,
            )

            # Prepare files list
            files_to_send = data.get("app_files", [])
            if not files_to_send and "app_file" in data:
                files_to_send = [data["app_file"]]

            for admin_id in full_admin_ids:
                if not admin_id.strip():
                    continue
                try:
                    bot.send_photo(
                        chat_id=admin_id,
                        photo=data["app_image"],
                        caption=admin_message,
                        reply_markup=markup,
                    )
                    for file_id in files_to_send:
                        bot.send_document(chat_id=admin_id, document=file_id)
                except Exception as e:
                    print(f"Error sending to admin {admin_id}: {e}")

        bot.delete_state(user_id, call.message.chat.id)

    elif call.data == "restart":
        bot.answer_callback_query(call.id, get_text("restarting"))
        del user_data[user_id]
        bot.delete_state(user_id, call.message.chat.id)
        start_command(call.message)


# --- Navigation Logic ---


@bot.callback_query_handler(func=lambda call: call.data == "go_back")
def go_back_callback(call):
    bot.answer_callback_query(call.id)
    go_back(call.message.chat.id, call.from_user.id)


def go_back(chat_id, user_id):
    state = bot.get_state(user_id, chat_id)
    data = user_data.get(user_id, {})

    # Logic to determine previous step and data to clear
    # Map: Current State -> (Previous Function, Key to Clear)

    if state == BotStates.app_type.name:
        # From App Type back to Post Type
        ask_post_type(chat_id, user_id)
        if "app_type" in data:
            del data["app_type"]

    elif state == BotStates.source.name:
        # From Source back to App Type
        ask_app_type(chat_id, user_id)
        if "source" in data:
            del data["source"]

    elif state == BotStates.publish_target.name:
        # From Publish Target back to Source
        ask_source(chat_id, user_id)
        if "publish_target" in data:
            del data["publish_target"]

    elif state == BotStates.app_name.name:
        # From App Name back to Publish Target
        ask_publish_target(chat_id, user_id)
        if "app_name" in data:
            del data["app_name"]

    elif state == BotStates.app_version.name:
        # From Version back to Name
        ask_app_name(chat_id, user_id)
        if "app_version" in data:
            del data["app_version"]

    elif state == BotStates.app_description.name:
        # From Desc back to Version
        ask_app_version(chat_id, user_id)
        if "app_description" in data:
            del data["app_description"]

    elif state == BotStates.translate_description.name:
        # From Translate Menu back to Desc
        ask_app_description(chat_id, user_id)
        if "translate_description" in data:
            del data["translate_description"]
        if "translation_mode" in data:
            del data["translation_mode"]

    elif state == BotStates.manual_translation.name:
        # From Manual Trans back to Translate Menu
        ask_translate_description(chat_id, user_id)
        if "english_description" in data:
            del data["english_description"]

    elif state == BotStates.mod_features.name:
        # From Mod Features back to...
        # We are leaving Mod Features, so clear it.
        if "mod_features" in data:
            del data["mod_features"]
        if "selected_features" in data:
            del data["selected_features"]

        publish_target = data.get("publish_target")
        translation_mode = data.get("translation_mode")

        if publish_target in ["english", "both"]:
            if translation_mode == "manual":
                ask_manual_translation(chat_id, user_id)
            else:  # auto
                ask_translate_description(chat_id, user_id)
        else:
            ask_app_description(chat_id, user_id)

    elif state == BotStates.english_mod_features.name:
        # From Eng Mod Features back to Mod Features
        ask_mod_features(chat_id, user_id)
        if "english_mod_features" in data:
            del data["english_mod_features"]

    elif state == BotStates.app_image.name:
        # From App Image back to... DYNAMIC
        if "app_image" in data:
            del data["app_image"]

        if data.get("post_type") == "game":
            # Games skip hashtag, so go back to Mod Features
            # Logic copied from old app_image handler
            publish_target = data.get("publish_target")
            translation_mode = data.get("translation_mode")

            if publish_target in ["english", "both"] and translation_mode == "manual":
                ask_english_mod_features(chat_id, user_id)
            else:
                ask_mod_features(chat_id, user_id)
                if translation_mode == "auto" and "english_mod_features" in data:
                    del data["english_mod_features"]
        else:
            ask_hashtag(chat_id, user_id)

    elif state == BotStates.hashtag.name:
        # From Hashtag back to Mod Features
        if "hashtag" in data:
            del data["hashtag"]

        publish_target = data.get("publish_target")
        translation_mode = data.get("translation_mode")

        if publish_target in ["english", "both"] and translation_mode == "manual":
            # Came from English Mod Features
            ask_english_mod_features(chat_id, user_id)
        else:
            # Came from Mod Features (Arabic or Auto-Translated)
            ask_mod_features(chat_id, user_id)

            if translation_mode == "auto" and "english_mod_features" in data:
                del data["english_mod_features"]

    elif state == BotStates.app_file.name:
        # From File back to...
        if "app_file" in data:
            del data["app_file"]
        if "app_files" in data:
            del data["app_files"]

        # Check if Auto-Filled Image exists (Skip Image step) or Manual (Go to Image)
        if data.get("auto_filled") and "app_image" in data:
            # Image was auto-filled, so we skipped ask_app_image.
            # Go back to Hashtag.
            ask_hashtag(chat_id, user_id)
        else:
            # Standard flow
            ask_app_image(chat_id, user_id)

    elif state == BotStates.confirmation.name:
        # From Confirm back to File
        ask_app_file(chat_id, user_id)
        # No data to clear for confirmation state

    else:
        # Default or Unknown state -> Start over
        bot.send_message(chat_id, "Error: Unknown state. Restarting.")
        ask_post_type(chat_id, user_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("admin_"))
def admin_approval_callback(call):
    action, user_id_str = call.data.split("_")[1:3]
    user_id = int(user_id_str)

    # Check if request is already processed (user_data missing)
    if user_id not in user_data:
        bot.answer_callback_query(
            call.id,
            "❌ عذراً، قام مشرف آخر باتخاذ الإجراء قبلك.",
            show_alert=True,
        )
        return

    original_poster_id = user_data[user_id].get("original_poster_id")

    if action == "approve":
        bot.answer_callback_query(call.id, "✅ تمت الموافقة")
        bot.edit_message_caption(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            caption="✅ تمت الموافقة",
        )

        # Publish the post
        data = user_data[user_id]
        publish_target = data.get("publish_target")

        # --- Dynamic Post Generation (Fit-to-Size) ---

        post_template_ar = ""
        post_template_en = ""

        if publish_target == "arabic" or publish_target == "both":
            # 1. Build Parts
            type_str = "تطبيق" if data.get("post_type") == "app" else "لعبة"
            source_str = (
                "مقترحات القناة"
                if data.get("source") == "recommendation"
                else "طلبات المشتركين"
            )
            mod_label = (
                "معدلة وفيها" if data.get("app_type") == "mod" else "النسخة رسمية"
            )

            part_top = f"🧩 {type_str}: {data.get('app_name')}\n📍من {source_str}"

            features_text = data.get("mod_features", "")
            part_bottom_template = "🧊 الإصدار:  {version}\n🏷 {mod_label}:\n{features}\n              ༺━━ @premium_techs ━━༻\nللتنزيل من هنا ⬇️ {hashtag}"
            part_bottom = part_bottom_template.format(
                version=data.get("app_version"),
                mod_label=mod_label,
                features=features_text,
                hashtag=data.get("hashtag"),
            )

            # 2. Check Overhead
            # Buffer = 20 (newlines and '⚡ الوصف : ')
            overhead = len(part_top) + len(part_bottom) + 20

            if overhead > 950:
                # Truncate features
                features_text = features_text[:400] + "..."
                part_bottom = part_bottom_template.format(
                    version=data.get("app_version"),
                    mod_label=mod_label,
                    features=features_text,
                    hashtag=data.get("hashtag"),
                )
                overhead = len(part_top) + len(part_bottom) + 20

            # 3. Calculate Available Space
            available_for_desc = max(50, 1024 - overhead)

            # 4. Truncate Description
            ar_desc = smart_truncate(
                data.get("app_description", ""), limit=available_for_desc
            )

            # 5. Assemble
            post_template_ar = f"{part_top}\n⚡ الوصف : {ar_desc}\n{part_bottom}"

        if publish_target == "english" or publish_target == "both":
            # 1. Build Parts
            type_str = "App" if data.get("post_type") == "app" else "Game"
            source_str = (
                "Channel Recommendation"
                if data.get("source") == "recommendation"
                else "Subscriber Request"
            )
            mod_label = (
                "Modded with" if data.get("app_type") == "mod" else "Official Version"
            )

            part_top = f"🧩 {type_str}: {data.get('app_name')}\n📍From: {source_str}"

            features_text = (
                data.get("english_mod_features")
                if "english_mod_features" in data
                else data.get("mod_features", "")
            )
            part_bottom_template = "🧊 Version: {version}\n🏷 {mod_label}:\n{features}\n              ༺━━ @premium_techs ━━༻\nDownload from here ⬇️ {hashtag}"
            part_bottom = part_bottom_template.format(
                version=data.get("app_version"),
                mod_label=mod_label,
                features=features_text,
                hashtag=data.get("hashtag"),
            )

            # 2. Check Overhead
            overhead = len(part_top) + len(part_bottom) + 20

            if overhead > 950:
                # Truncate features
                features_text = features_text[:400] + "..."
                part_bottom = part_bottom_template.format(
                    version=data.get("app_version"),
                    mod_label=mod_label,
                    features=features_text,
                    hashtag=data.get("hashtag"),
                )
                overhead = len(part_top) + len(part_bottom) + 20

            # 3. Calculate Available Space
            available_for_desc = max(50, 1024 - overhead)

            # 4. Truncate Description
            en_desc_raw = (
                data.get("english_description")
                if "english_description" in data
                else data.get("app_description", "")
            )
            en_desc = smart_truncate(en_desc_raw, limit=available_for_desc)

            # 5. Assemble
            post_template_en = f"{part_top}\n⚡ Description: {en_desc}\n{part_bottom}"

        # Prepare files list
        files_to_send = data.get("app_files", [])
        if not files_to_send and "app_file" in data:
            files_to_send = [data["app_file"]]

        if publish_target == "arabic" or publish_target == "both":
            channel_id = os.environ.get("ARABIC_CHANNEL_ID")
            bot.send_photo(
                chat_id=channel_id, photo=data["app_image"], caption=post_template_ar
            )

            last_msg_id = None
            for file_id in files_to_send:
                sent_doc = bot.send_document(chat_id=channel_id, document=file_id)
                last_msg_id = sent_doc.message_id

            if last_msg_id:
                try:
                    bot.send_poll(
                        chat_id=channel_id,
                        question=get_text("poll_question", "ar"),
                        options=get_text("poll_options", "ar"),
                        is_anonymous=True,
                        reply_to_message_id=last_msg_id,
                    )
                except Exception as e:
                    print(f"Error sending poll: {e}")

        if publish_target == "english" or publish_target == "both":
            channel_id = os.environ.get("ENGLISH_CHANNEL_ID")
            bot.send_photo(
                chat_id=channel_id, photo=data["app_image"], caption=post_template_en
            )

            last_msg_id = None
            for file_id in files_to_send:
                sent_doc = bot.send_document(chat_id=channel_id, document=file_id)
                last_msg_id = sent_doc.message_id

            if last_msg_id:
                try:
                    bot.send_poll(
                        chat_id=channel_id,
                        question=get_text("poll_question", "en"),
                        options=get_text("poll_options", "en"),
                        is_anonymous=True,
                        reply_to_message_id=last_msg_id,
                    )
                except Exception as e:
                    print(f"Error sending poll: {e}")

        # Broadcast Notification
        submitter_name = user_data[user_id].get("submitter_name", "Unknown")
        app_name_notify = user_data[user_id].get("app_name", "App")
        admin_name = call.from_user.first_name

        broadcast_msg = f"✅ تم نشر التطبيق **{app_name_notify}** بواسطة **{submitter_name}** واعتماده من قبل المشرف **{admin_name}**."

        admin_raw = os.environ.get("FULL_ADMIN_ID", "")
        full_admin_ids = [i.strip() for i in admin_raw.split(",") if i.strip()]
        acting_admin_id = str(call.from_user.id)

        for admin_id in full_admin_ids:
            admin_id = admin_id.strip()
            if admin_id and admin_id != acting_admin_id:
                try:
                    bot.send_message(admin_id, broadcast_msg, parse_mode="Markdown")
                except Exception as e:
                    print(f"Error broadcasting to admin {admin_id}: {e}")

        if original_poster_id:
            bot.send_message(original_poster_id, "✅ تم النشر! اكتب /start للبدء")
            try:
                bot.send_message(original_poster_id, broadcast_msg, parse_mode="Markdown")
            except Exception as e:
                print(f"Error sending broadcast to submitter: {e}")

        if user_id in user_data:
            del user_data[user_id]
        bot.delete_state(user_id)

    elif action == "reject":
        admin_id = call.from_user.id
        if admin_id not in user_data:
            user_data[admin_id] = {}

        user_data[admin_id]["rejecting_target"] = user_id
        user_data[admin_id]["rejecting_message_id"] = call.message.message_id

        bot.set_state(admin_id, BotStates.admin_rejection_reason, call.message.chat.id)

        markup = quick_markup(
            {get_text("cancel_button"): {"callback_data": "admin_cancel_rejection"}}
        )

        bot.send_message(
            call.message.chat.id, get_text("ask_rejection_reason"), reply_markup=markup
        )


@bot.callback_query_handler(func=lambda call: call.data == "admin_cancel_rejection")
def admin_cancel_rejection_callback(call):
    admin_id = call.from_user.id

    # Cleanup admin state
    bot.delete_state(admin_id, call.message.chat.id)

    # Cleanup temp data
    if admin_id in user_data:
        user_data[admin_id].pop("rejecting_target", None)
        user_data[admin_id].pop("rejecting_message_id", None)

    bot.answer_callback_query(call.id, get_text("rejection_cancelled"))
    bot.delete_message(call.message.chat.id, call.message.message_id)


@bot.message_handler(state=BotStates.admin_rejection_reason)
def admin_rejection_reason_handler(message):
    admin_id = message.from_user.id

    # Retrieve rejection details
    if admin_id not in user_data or "rejecting_target" not in user_data[admin_id]:
        # Should not happen if state is consistent, but safety check
        bot.delete_state(admin_id, message.chat.id)
        return

    target_user_id = user_data[admin_id]["rejecting_target"]

    # Check if request is still valid (not processed by another admin)
    if target_user_id not in user_data:
        bot.send_message(
            message.chat.id, "⛔ Request already processed by another admin."
        )
        bot.delete_state(admin_id, message.chat.id)
        user_data[admin_id].pop("rejecting_target", None)
        user_data[admin_id].pop("rejecting_message_id", None)
        return

    reject_message_id = user_data[admin_id].get("rejecting_message_id")
    rejection_reason = message.text

    # Action 1: Notify User
    # Retrieve original_poster_id if available (or use target_user_id)

    original_poster_id = target_user_id

    notification_text = get_text("rejection_notification") + rejection_reason
    try:
        bot.send_message(original_poster_id, notification_text)
    except Exception as e:
        print(f"Error sending rejection to user {original_poster_id}: {e}")

    # Action 2: Edit Admin Message
    if reject_message_id:
        try:
            bot.edit_message_caption(
                chat_id=message.chat.id,
                message_id=reject_message_id,
                caption=f"Rejected: {rejection_reason}",
                reply_markup=None,  # Remove buttons
            )
        except Exception as e:
            print(f"Error updating admin message: {e}")
            bot.send_message(message.chat.id, get_text("error_missing_data_msg_update"))

    # Action 3: Cleanup
    bot.send_message(message.chat.id, get_text("rejection_sent"))

    # Clear user data for the rejected submission
    if target_user_id in user_data:
        del user_data[target_user_id]
        bot.delete_state(target_user_id)  # Also clear their state if any

    # Clear admin temp data and state
    user_data[admin_id].pop("rejecting_target", None)
    user_data[admin_id].pop("rejecting_message_id", None)
    bot.delete_state(admin_id, message.chat.id)


# --- Auto-Mirroring (Arabic Channel -> English Channel) ---


def translate_text(text):
    """
    Translates text to English using GoogleTranslator.
    Returns original text if translation fails or text is None/Empty.
    """
    if not text:
        return ""
    try:
        return GoogleTranslator(source="auto", target="en").translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # Fallback to original


@bot.channel_post_handler(content_types=["photo", "document", "poll"])
def auto_mirror_channel_post(message):
    arabic_channel_id_str = os.environ.get("ARABIC_CHANNEL_ID")
    english_channel_id_str = os.environ.get("ENGLISH_CHANNEL_ID")

    if not arabic_channel_id_str or not english_channel_id_str:
        return

    arabic_channel_id = int(arabic_channel_id_str)
    english_channel_id = int(english_channel_id_str)

    # Guard: Only process posts from the Arabic Channel
    if message.chat.id != arabic_channel_id:
        return

    try:
        if message.content_type == "photo":
            # Photos: Get largest photo and translate caption
            file_id = message.photo[-1].file_id
            english_caption = translate_text(message.caption)
            bot.send_photo(
                chat_id=english_channel_id, photo=file_id, caption=english_caption
            )

        elif message.content_type == "document":
            # Documents: Get file_id and translate caption
            file_id = message.document.file_id
            english_caption = translate_text(message.caption)
            bot.send_document(
                chat_id=english_channel_id, document=file_id, caption=english_caption
            )

        elif message.content_type == "poll":
            try:
                # Polls: Use standard English "Rate this app" template
                original_poll = message.poll

                english_question = get_text("poll_question", "en")
                english_options = get_text("poll_options", "en")

                bot.send_poll(
                    chat_id=english_channel_id,
                    question=english_question,
                    options=english_options,
                    is_anonymous=original_poll.is_anonymous,
                    type="regular",
                    allows_multiple_answers=False,
                    open_period=original_poll.open_period,
                    close_date=original_poll.close_date,
                    is_closed=original_poll.is_closed,
                )
            except Exception as e:
                print(f"Error mirroring poll: {e}")

    except Exception as e:
        print(f"Error in auto-mirroring: {e}")
