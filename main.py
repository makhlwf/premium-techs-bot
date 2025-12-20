import os
import telebot
from telebot.handler_backends import State, StatesGroup
from telebot import custom_filters
from telebot.util import quick_markup
from dotenv import load_dotenv
from googletrans import Translator
import asyncio
import nest_asyncio

nest_asyncio.apply()

# --- Translation System ---
translations = {
    "ar": {
        "welcome": "أهلاً بك في بوت premium-techs-bot!",
        "start_button": "ابدأ",
        "unauthorized": "أنت غير مصرح لك باستخدام هذا البوت.",
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
        "mod_features_question": "الرجاء إدخال ميزات التعديل (باللغة العربية).",
        "app_image_question": "الرجاء إرسال صورة التطبيق.",
        "hashtag_question": "الرجاء اختيار هاشتاج للتطبيق:",
        "app_file_question": "الرجاء رفع ملف التطبيق.",
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
    },
}

def get_text(key, lang="ar"):
    return translations[lang][key]

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
    app_version = State()
    app_description = State()
    translate_description = State()
    manual_translation = State()
    mod_features = State()
    app_image = State()
    hashtag = State()
    app_file = State()
    confirmation = State()
    admin_approval = State()


async def main():
    bot = telebot.TeleBot(os.environ.get("BOT_TOKEN"), use_class_middlewares=True)
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    translator = Translator()

    @bot.message_handler(commands=['start'])
    def start_command(message):
        allowed_posters_ids = os.environ.get("ALLOWED_POSTERS_IDS", "").split(',')
        full_admin_id = os.environ.get("FULL_ADMIN_ID")
        
        if str(message.from_user.id) not in allowed_posters_ids and str(message.from_user.id) != full_admin_id:
            bot.send_message(message.chat.id, get_text("unauthorized"))
            return
        
        markup = quick_markup({get_text("start_button"): {'callback_data': 'start_conversation'}})
        bot.send_message(message.chat.id, get_text("welcome"), reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data == 'start_conversation')
    def start_conversation_callback(call):
        bot.set_state(call.from_user.id, BotStates.post_type, call.message.chat.id)
        markup = quick_markup({
            get_text("app_button"): {'callback_data': 'post_type_app'},
            get_text("game_button"): {'callback_data': 'post_type_game'}
        }, row_width=2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=get_text("post_type_question"), reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('post_type_'))
    def post_type_callback(call):
        user_id = call.from_user.id
        user_data[user_id] = {'post_type': call.data.split('_')[2], 'original_poster_id': user_id}
        bot.answer_callback_query(call.id, f"لقد اخترت: {user_data[user_id]['post_type']}")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=get_text("great_next_step"))
        bot.set_state(user_id, BotStates.app_type, call.message.chat.id)
        markup = quick_markup({
            get_text("mod_button"): {'callback_data': 'app_type_mod'},
            get_text("official_button"): {'callback_data': 'app_type_official'}
        }, row_width=2)
        bot.send_message(call.message.chat.id, get_text("app_type_question"), reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('app_type_'))
    def app_type_callback(call):
        user_id = call.from_user.id
        user_data[user_id]['app_type'] = call.data.split('_')[2]
        bot.answer_callback_query(call.id, f"لقد اخترت: {user_data[user_id]['app_type']}")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=get_text("great_next_step"))
        bot.set_state(user_id, BotStates.source, call.message.chat.id)
        markup = quick_markup({
            get_text("channel_recommendation"): {'callback_data': 'source_recommendation'},
            get_text("subscriber_request"): {'callback_data': 'source_request'}
        }, row_width=2)
        bot.send_message(call.message.chat.id, get_text("source_question"), reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('source_'))
    def source_callback(call):
        user_id = call.from_user.id
        user_data[user_id]['source'] = call.data.split('_')[1]
        bot.answer_callback_query(call.id, f"لقد اخترت: {user_data[user_id]['source']}")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=get_text("got_it"))
        bot.set_state(user_id, BotStates.publish_target, call.message.chat.id)
        markup = quick_markup({
            get_text("arabic_button"): {'callback_data': 'publish_arabic'},
            get_text("english_button"): {'callback_data': 'publish_english'},
            get_text("both_button"): {'callback_data': 'publish_both'}
        }, row_width=3)
        bot.send_message(call.message.chat.id, get_text("publish_target_question"), reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('publish_'))
    def publish_target_callback(call):
        user_id = call.from_user.id
        user_data[user_id]['publish_target'] = call.data.split('_')[1]
        bot.answer_callback_query(call.id, f"لقد اخترت: {user_data[user_id]['publish_target']}")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=get_text("awesome"))
        bot.set_state(user_id, BotStates.app_name, call.message.chat.id)
        bot.send_message(call.message.chat.id, get_text("app_name_question"))

    @bot.message_handler(state=BotStates.app_name)
    def app_name_handler(message):
        user_id = message.from_user.id
        user_data[user_id]['app_name'] = message.text
        bot.set_state(user_id, BotStates.app_version, message.chat.id)
        bot.send_message(message.chat.id, get_text("app_version_question"))

    @bot.message_handler(state=BotStates.app_version)
    def app_version_handler(message):
        user_id = message.from_user.id
        user_data[user_id]['app_version'] = message.text
        bot.set_state(user_id, BotStates.app_description, message.chat.id)
        bot.send_message(message.chat.id, get_text("app_description_question"))

    @bot.message_handler(state=BotStates.app_description)
    def app_description_handler(message):
        user_id = message.from_user.id
        user_data[user_id]['app_description'] = message.text
        if user_data[user_id].get('publish_target') == 'both':
            bot.set_state(user_id, BotStates.translate_description, message.chat.id)
            markup = quick_markup({
                get_text("manual_button"): {'callback_data': 'translate_manual'},
                get_text("auto_button"): {'callback_data': 'translate_auto'}
            }, row_width=2)
            bot.send_message(message.chat.id, get_text("translate_question"), reply_markup=markup)
        else:
            bot.set_state(user_id, BotStates.mod_features, message.chat.id)
            bot.send_message(message.chat.id, get_text("mod_features_question"))

    @bot.callback_query_handler(state=BotStates.translate_description)
    async def translate_description_callback(call):
        user_id = call.from_user.id
        if call.data == 'translate_manual':
            bot.answer_callback_query(call.id, "لقد اخترت: يدوياً")
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=get_text("manual_translation_prompt"))
            bot.set_state(user_id, BotStates.manual_translation, call.message.chat.id)
        elif call.data == 'translate_auto':
            user_data[user_id]['translate_description'] = 'auto'
            bot.answer_callback_query(call.id, "لقد اخترت: تلقائياً")
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=get_text("auto_translation_used"))
            
            # Perform auto translation
            try:
                translated = await translator.translate(user_data[user_id]['app_description'], dest='en')
                user_data[user_id]['english_description'] = translated.text
            except Exception as e:
                print(f"Translation error: {e}")
                user_data[user_id]['english_description'] = "Translation failed."

            bot.set_state(user_id, BotStates.mod_features, call.message.chat.id)
            bot.send_message(call.message.chat.id, get_text("mod_features_question"))

    @bot.message_handler(state=BotStates.manual_translation)
    def manual_translation_handler(message):
        user_id = message.from_user.id
        user_data[user_id]['english_description'] = message.text
        bot.set_state(user_id, BotStates.mod_features, message.chat.id)
        bot.send_message(message.chat.id, get_text("mod_features_question"))

    @bot.message_handler(state=BotStates.mod_features)
    def mod_features_handler(message):
        user_id = message.from_user.id
        user_data[user_id]['mod_features'] = message.text
        bot.set_state(user_id, BotStates.app_image, message.chat.id)
        bot.send_message(message.chat.id, get_text("app_image_question"))

        @bot.message_handler(state=BotStates.app_image, content_types=['photo'])

        def app_image_handler(message):

            user_id = message.from_user.id

            user_data[user_id]['app_image'] = message.photo[-1].file_id

    

            if user_data[user_id].get('post_type') == 'game':

                user_data[user_id]['hashtag'] = '#games'

                bot.set_state(user_id, BotStates.app_file, message.chat.id)

                bot.send_message(message.chat.id, get_text("app_file_question"))

            else:

                bot.set_state(user_id, BotStates.hashtag, message.chat.id)

                hashtags = {

                    'تواصل اجتماعي': {'callback_data': '#Social'}, 'تعديل': {'callback_data': '#editing'},

                    'VPN': {'callback_data': '#vpn'}, 'أدوات': {'callback_data': '#Tools'},

                    'مشاهدة': {'callback_data': '#watching'}, 'وسائط متعددة': {'callback_data': '#multimedia'},

                    'متصفح': {'callback_data': '#browser'}, 'ترجمة': {'callback_data': '#translate'},

                    'متجر': {'callback_data': '#store'}, 'تسجيل': {'callback_data': '#record'},

                    'نصائح': {'callback_data': '#tips'}, 'كتب': {'callback_data': '#books'},

                    'خلفيات': {'callback_data': '#wallpapers'}, 'ثيمات': {'callback_data': '#themes'},

                    'تعليم': {'callback_data': '#learning'}, 'ديني': {'callback_data': '#religious'},

                    'أخبار': {'callback_data': '#news'}, 'موسيقى': {'callback_data': '#music'},

                    'كيبورد': {'callback_data': '#keyboard'}, 'كاميرا': {'callback_data': '#camera'},

                    'ذكاء اصطناعي': {'callback_data': '#AI'}

                }

                markup = quick_markup(hashtags, row_width=3)

                bot.send_message(message.chat.id, get_text("hashtag_question"), reply_markup=markup)

    @bot.callback_query_handler(state=BotStates.hashtag)
    def hashtag_callback(call):
        user_id = call.from_user.id
        user_data[user_id]['hashtag'] = call.data
        bot.answer_callback_query(call.id, f"لقد اخترت: {call.data}")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=get_text("awesome"))
        bot.set_state(user_id, BotStates.app_file, call.message.chat.id)
        bot.send_message(call.message.chat.id, get_text("app_file_question"))

    @bot.message_handler(state=BotStates.app_file, content_types=['document'])
    def app_file_handler(message):
        user_id = message.from_user.id
        user_data[user_id]['app_file'] = message.document.file_id
        bot.set_state(user_id, BotStates.confirmation, message.chat.id)
        data = user_data[user_id]
        confirmation_message = f"""{get_text("review_prompt")}

نوع التطبيق: {data.get('app_type')}
المصدر: {data.get('source')}
وجهة النشر: {data.get('publish_target')}
اسم التطبيق: {data.get('app_name')}
إصدار التطبيق: {data.get('app_version')}
وصف التطبيق: {data.get('app_description')}
الهاشتاج: {data.get('hashtag')}
"""
        if 'english_description' in data:
            confirmation_message += f"الوصف باللغة الإنجليزية: {data.get('english_description')}\n"
        if 'mod_features' in data:
            confirmation_message += f"ميزات التعديل: {data.get('mod_features')}\n"

        markup = quick_markup({
            get_text("confirm_button"): {'callback_data': 'confirm'},
            get_text("restart_button"): {'callback_data': 'restart'}
        }, row_width=2)
        bot.send_photo(chat_id=message.chat.id, photo=data['app_image'], caption=confirmation_message, reply_markup=markup)

    @bot.callback_query_handler(state=BotStates.confirmation)
    def confirmation_callback(call):
        user_id = call.from_user.id
        if call.data == 'confirm':
            bot.answer_callback_query(call.id, get_text("request_submitted"))
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=get_text("request_pending"))
            
            # Send to full admin for approval
            full_admin_id = os.environ.get("FULL_ADMIN_ID")
            if full_admin_id:
                data = user_data[user_id]
                admin_message = f"{get_text('new_submission')} {call.from_user.first_name}:\n\n{call.message.caption}"
                markup = quick_markup({
                    get_text("approve_button"): {'callback_data': f'admin_approve_{user_id}'},
                    get_text("reject_button"): {'callback_data': f'admin_reject_{user_id}'}
                }, row_width=2)
                bot.send_photo(chat_id=full_admin_id, photo=data['app_image'], caption=admin_message, reply_markup=markup)
                bot.send_document(chat_id=full_admin_id, document=data['app_file'])

            bot.delete_state(user_id, call.message.chat.id)

        elif call.data == 'restart':
            bot.answer_callback_query(call.id, get_text("restarting"))
            del user_data[user_id]
            bot.delete_state(user_id, call.message.chat.id)
            start_command(call.message)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('admin_'))
    def admin_approval_callback(call):
        action, user_id_str = call.data.split('_')[1:3]
        user_id = int(user_id_str)
        original_poster_id = user_data[user_id].get('original_poster_id')

        if action == 'approve':
            bot.answer_callback_query(call.id, "Approved")
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption="Approved")
            
            # Publish the post
            data = user_data[user_id]
            publish_target = data.get('publish_target')
            
            post_template_ar = f"""🧩 { 'تطبيق' if data.get('post_type') == 'app' else 'لعبة'} {data.get('app_name')}
📍من { 'مقترحات القناة' if data.get('source') == 'recommendation' else 'طلبات المشتركين'} 
⚡ الوصف : {data.get('app_description')}
🧊 الإصدار:  {data.get('app_version')}
🏷 {'معدلة وفيها' if data.get('app_type') == 'mod' else 'النسخة رسمية'}:  
✓ {data.get('mod_features')}
              ༺━━ @premium_techs ━━༻
للتنزيل من هنا ⬇️ {data.get('hashtag')}
"""
            
            post_template_en = f"""🧩 { 'App' if data.get('post_type') == 'app' else 'Game'}: {data.get('app_name')}
📍From: { 'Channel Recommendation' if data.get('source') == 'recommendation' else 'Subscriber Request'}
⚡ Description: {data.get('english_description') if 'english_description' in data else data.get('app_description')}
🧊 Version: {data.get('app_version')}
🏷 {'Modded with' if data.get('app_type') == 'mod' else 'Official Version'}:
✓ {data.get('mod_features')}
              ༺━━ @premium_techs ━━༻
Download from here ⬇️ {data.get('hashtag')}
"""
            if publish_target == 'arabic' or publish_target == 'both':
                channel_id = os.environ.get("ARABIC_CHANNEL_ID")
                bot.send_photo(chat_id=channel_id, photo=data['app_image'], caption=post_template_ar)
                bot.send_document(chat_id=channel_id, document=data['app_file'])

            if publish_target == 'english' or publish_target == 'both':
                channel_id = os.environ.get("ENGLISH_CHANNEL_ID")
                bot.send_photo(chat_id=channel_id, photo=data['app_image'], caption=post_template_en)
                bot.send_document(chat_id=channel_id, document=data['app_file'])
            
            if original_poster_id:
                bot.send_message(original_poster_id, get_text("post_approved"))

        elif action == 'reject':
            bot.answer_callback_query(call.id, "Rejected")
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption="Rejected")
            if original_poster_id:
                bot.send_message(original_poster_id, get_text("post_rejected"))

        bot.delete_state(user_id)
    
    print("Bot is polling...")
    await bot.polling(skip_pending=True)


if __name__ == "__main__":
    asyncio.run(main())
