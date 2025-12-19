# premium-techs-bot
the open source version of a telegram bot to help the admins of premium techs telegram channel

# how to develop
1. clone the repo
2. insure you have uv installed
```
pip install uv
```
3. cd to the project and run
```
uv sync
```
4. edit `.env.example` add your values and remove .example from the file name
5. run
```
uv run main.py
```
and test your changes

# what to do
- [x] Ask the user whether the app is mod or official
- [x] Ask the user whether the app is from channel recommendations or subscriber requests
- [x] Ask the user whether they want to publish it in the Arabic channel only, the English channel only, or both
- [x] Ask the user for the app name
- [x] Ask the user for the app version
- [x] Ask the user for the app description
- [x] If the user chose to publish in both channels, ask whether they already have an English translation of the Arabic description to enter manually, or if it should be translated using Google Translate or a free daily AI translation API (posting volume is low, so limits won’t be reached)
- [x] Ask the user about the mods in the modded version (the translation feature mentioned above may be added here)
- [ ] Ask the user for the app image; if they don’t have one, provide an option to fetch it from Google Play or sites like APKPure, APKCombo, or APKMirror
- [x] Ask the user to choose a hashtag for the app
- [x] Ask the user for the app file; currently, there are not enough resources to rename the file or change its icon, so the user will be directed to an external bot (most moderators already know this workflow)
- [x] Ask the user whether they want to proceed once all information is provided or restart from the beginning
- [x] Send the collected information to specific, highly trusted moderators for review
- [x] Give moderators the option to approve and publish, or reject and send a reason
- [x] If approved, the bot automatically publishes the post to the channel using the predefined template and filled-in information
- [x] The bot also publishes the file using a Telegram API feature that may allow file copying, avoiding re-uploading since the file already exists on Telegram servers, and allowing caption editing
- [ ] Publish a poll post using interactive buttons to collect user ratings, which will be reviewed monthly to analyze posting preferences
- [x] If a moderator chooses to reject the post, they must write a rejection reason, which will be sent to the submitter and other moderators

# some information
here is some info to help you out
1. we use PyTelegramBotAPI for telegram bot interactions
2. the posts tamplate are as followes
```
🧩 تطبيق 
📍من طلبات المشتركين 
⚡ الوصف : 
🧊 الإصدار:  
🏷 معدلة وفيها :  
✓
              ༺━━ @premium_techs ━━༻
للتنزيل من هنا ⬇️ #hashtag
```
use 
```
📍من مقترحات القناة
```
if it is a recomendation
also use
```
🎮 لعبة  
```
if it is a game
and use
```
🏷 النسخة رسمية :
```
if it is an official app
# hashtags
```
• العاب متنوعة و متعددة   ⬅️ #games
•  للتواصل الاجتماعي ..     ⬅️ #Social
•  برامج للمنتاج و التصميم ⬅️ #editing
• لـ VPN (كاسر بروكسي)  ⬅️ #vpn
• لادوات و مميزات متنوعة ⬅️ #Tools
• لمشاهدة الافلام والقنوات ⬅️ #watching
• لتشغيل الافلام و الفيديو  ⬅️ #multimedia
• متصفحات انترنت متنوعة⬅️ #browser
• للترجمة و معنى الكلمات   ⬅️  #translate
• لمتاجر تطبيقات و العاب   ⬅️ #store
• لتسجيل الصوت و الفيديو⬅️ #record
• للشروحات و النصائح  ...  ⬅️ #tips
• قراءة الكتب و تنزيلها  ...  ⬅️ #books
• خلفيات الشاشة متنوعة..  ⬅️ #wallpapers
• ثيمات و واجهات نظام ..   ⬅️ #themes
• للتعلم ( برمجة /لغات /..) ⬅️ #learning
• الامور و الكتب الدينية ..   ⬅️ #religious
• للاخبار و المعلومات  ......  ⬅️ #news
• استماع للموسيقى  .......   ⬅️ #music
• كيبوردات متنوعة للهاتف ..⬅️ #keyboard
• تطبيقات للتصوير و الفلاتر ⬅️ #camera
. تطبيقات ذكاء اصطناعي.   ⬅️  #AI
```
translate to english respectively