# 🤖 Premium Techs Publisher Bot - Project

### **1. Project Overview**

A professional-grade Telegram bot designed to automate the publishing of Apps and Games to specific Telegram channels. The bot features a bilingual workflow (Arabic/English), intelligent auto-filling from Google Play, automatic translation, and a robust approval system.

---

### **2. Key Features Implemented**

#### **🚀 Smart Auto-Fill & Scraping**

* **Hybrid Search Engine:** Users can enter a direct Google Play **Link** OR just an **App Name**. The bot scrapes the store to find the correct app.
* **Deep Fetch:** Retrieves comprehensive data including **App Icon, Title, Short Description, Long Description (About), and Recent Changes**.
* **Intelligent Translation:** Scrapes the *English* store (for higher quality data) and automatically translates it to *Arabic* for the user.
* **Interactive Editor:** Before saving, users can preview the scraped data and use an **"Edit Panel"** to modify the Name, Description, or Image manually.

#### **📝 Content Management**

* **Multi-Select "Mod Features":** A dynamic Inline Menu to select features (e.g., `✓ Premium`, `✓ No Ads`) or type custom ones.
* **Hashtag Selector:** A dedicated menu for categorizing apps (e.g., `#Social`, `#Tools`).
* **Auto-Translation:** Automatically translates descriptions and mod features from Arabic to English (or vice versa) based on the target channel.

#### **📢 Publishing & Automation**

* **Dual-Channel Publishing:** Can post to an **Arabic Channel**, an **English Channel**, or **Both** simultaneously with correct formatting for each.
* **Auto-Mirroring:** If an Admin posts a Photo, File, or Poll directly to the *Arabic Channel*, the bot detects it, translates the caption to English, and mirrors it to the *English Channel* automatically.
* **Admin Approval System:** All user submissions are sent to a "Full Admin" for review (Approve/Reject) before going live.

#### **🛡️ Stability & Architecture**

* **Dynamic Layout Engine:** A smart algorithm that calculates the exact length of the Description to ensure the post never exceeds Telegram's **1024-character limit**, while guaranteeing the **Download Link (Footer)** is never cut off.
* **Robust Navigation:** A generic "Back" button system that handles complex state jumps (e.g., skipping steps when using Auto-Fill).
* **Crash Protection:** Fail-safe truncation logic to prevent API errors (400 Bad Request) when handling massive descriptions.

---

### **3. Development Timeline :**

 **Foundation**  • Initialized Bot structure (Telebot).<br>

<br>• Created State Machine (Name -> Version -> Desc -> File).<br>

<br>• Designed Post Templates for Arabic/English. 
 **Translation**  • Integrated `deep-translator` for robust language support.<br>

<br>• Added logic to auto-translate descriptions if the target is "English" or "Both".<br>

<br>• Implemented the first version of the "Back" button. 
 **Automation**  • **Auto-Mirroring:** Created the "Channel Post Handler" to listen to the Arabic channel and forward translated copies to the English channel. 
 **UI Polish**  • **Mod Features Builder:** Created the checkbox-style menu for selecting multiple features.<br>

<br>• **Formatting:** Standardized output to use `✓` for features and `#` for hashtags. 
 **Intelligence**  • **Smart Auto-Fill:** Implemented Google Play scraping.<br>

<br>• **Deep Fetch:** Upgraded to `google-play-scraper` library to fetch massive details.<br>

<br>• **Edit Panel:** Added buttons to Edit Name/Desc/Image inside the Auto-Fill preview. 
 **Stability**  • **Crash Fixes:** Solved the "Caption Too Long" API crash.<br>

<br>• **Flow Repair:** Re-wired the navigation (Mod -> Hashtag -> Image) to ensure no steps are skipped.<br>

<br>• **Fit-to-Size Engine:** Implemented the final dynamic calculation to preserve the Footer in long posts. 

---

### **4. Technical Stack**

* **Framework:** Python (`pyTelegramBotAPI`)
* **Hosting:** Vercel (Serverless Architecture)
* **Scraping:** `google-play-scraper`, `requests`, `BeautifulSoup`
* **Translation:** `deep-translator` (Google Translate API)
* **Database:** In-Memory `user_data` (optimized for session-based workflows)

---

### **5. How to Use (User Guide)**

1. **Start:** Send `/start` to begin.
2. **Auto-Fill:** When asked for the name, click **"⚡️ Auto Fill"**.
3. **Input:** Type the App Name (e.g., "Telegram") or paste a Google Play Link.
4. **Review:** Use **"📜 Deep Fetch"** to see all details. Use **"✏️ Edit"** buttons to tweak data. Click **"✅ Approve"**.
5. **Finalize:** Enter Version and select Mod Features.
6. **Publish:** Upload the file and confirm. The Admin receives the request and clicks **"Approve"** to publish to channels.

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
* [x] Ask the user whether the app is mod or official
* [x] Ask the user whether the app is from channel recommendations or subscriber requests
* [x] Ask the user whether they want to publish it in the Arabic channel only, the English channel only, or both
* [x] Ask the user for the app name
* [x] Ask the user for the app version
* [x] Ask the user for the app description
* [x] If the user chose to publish in both channels, ask whether they already have an English translation of the Arabic description to enter manually, or if it should be translated using Google Translate or a free daily AI translation API (posting volume is low, so limits won’t be reached)
* [x] Ask the user about the mods in the modded version (the translation feature mentioned above may be added here)
* [x] Ask the user for the app image; if they don’t have one, provide an option to fetch it from Google Play or sites like APKPure, APKCombo, or APKMirror
* [x] Ask the user to choose a hashtag for the app
* [x] Ask the user for the app file; currently, there are not enough resources to rename the file or change its icon, so the user will be directed to an external bot (most moderators already know this workflow)
* [x] Ask the user whether they want to proceed once all information is provided or restart from the beginning
* [x] Send the collected information to specific, highly trusted moderators for review
* [x] Give moderators the option to approve and publish, or reject and send a reason
* [x] If approved, the bot automatically publishes the post to the channel using the predefined template and filled-in information
* [x] The bot also publishes the file using a Telegram API feature that may allow file copying, avoiding re-uploading since the file already exists on Telegram servers, and allowing caption editing
* [x] Publish a poll post using interactive buttons to collect user ratings, which will be reviewed monthly to analyze posting preferences
* [x] If a moderator chooses to reject the post, they must write a rejection reason, which will be sent to the submitter and other moderators

* [x] **Post Type & App Type:** Ask if the app is Mod/Official and App/Game.
* [x] **Source Tracking:** Ask if the post is from Channel Recommendations or Subscriber Requests.
* [x] **Publishing Target:** Support publishing to **Arabic Only**, **English Only**, or **Both**.
* [x] **Basic Inputs:** Collect App Name and Version manually.
* [x] **Description & Translation:**
* [x] Collect Arabic Description.
* [x] If target is English/Both, offer **Auto-Translation** (via `deep-translator`) or Manual Input.


* [x] **Mod Features:**
* [x] Created a **Multi-Select Menu** (Checkbox style) for features (e.g., `✓ Premium`, `✓ No Ads`).
* [x] Allowed users to type **Custom Features** manually.
* [x] Auto-translates features to English if needed.


* [x] **Hashtags:** Created a menu for category selection (e.g., `#Social`, `#Tools`) + Custom hashtag input.

* [x] **Hybrid Search Engine:** Allows searching by **App Name** OR **Google Play Link**.
* [x] **Deep Fetch:** Scrapes the **English Play Store** (for quality) and auto-translates to Arabic.
* [x] Fetches Title, Icon, Short Description, Long Description, and Recent Changes.


* [x] **Interactive Preview:** Shows a preview card with **Edit Buttons** (Edit Name, Desc, Image) before confirming.
* [x] **Workflow Shortcuts:** If Auto-Fill is used, the bot intelligently **skips** the manual Name, Description, and Image steps to save time.

* [x] **Admin Approval Workflow:**
* [x] Sends full preview (Photo + Caption + File) to the Admin.
* [x] Admin can **Approve** (Publish) or **Reject** (with a reason sent to the user).


* [x] **Dual-Channel Publishing:**
* [x] Posts to the **Arabic Channel** with Arabic Template.
* [x] Posts to the **English Channel** with English Template.
* [x] Posts the **Poll** automatically after the file.


* [x] **Auto-Mirroring:**
* [x] Detects when an Admin posts a Photo/File/Poll directly to the Arabic Channel.
* [x] Automatically translates the caption and forwards it to the English Channel.

* [x] **Crash Protection:** Implemented a **"Fit-to-Size" Engine** to prevent Telegram API errors (Limit 1024 chars).
* [x] Dynamically calculates available space.
* [x] Truncates the Description intelligently to ensure the **Footer (Download Link)** is NEVER cut off.


* [x] **Navigation System:** Added a universal **[Back]** button logic that handles complex jumps (e.g., going back from File -> Hashtag when Image was skipped).
* [x] **Data Integrity:** Switched to `google-play-scraper` library to ensure "What's New" text doesn't accidentally replace the main description.


# some information
here is some info to help you out
1. we use PyTelegramBotAPI for telegram bot interactions
2. the posts tamplate are as followes
```
🧩 تطبيق : 
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
