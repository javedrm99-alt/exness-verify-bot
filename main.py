import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ================= AUTOMATIC SETTINGS BY AI =================
BOT_TOKEN = "8615620812:AAExMExwJPDna6h5oWZtcbn7fefxY8CITbs"  # आपका बोट टोकन सेट है
VIP_GROUP_LINK = "https://t.me"             # आपका ग्रुप लिंक सेट है
ADMIN_ID = 1124451959                                        # आपकी टेलीग्राम आईडी सेट है
# ============================================================

DB_FILE = "users.txt"

def load_registered_uids():
    if not os.path.exists(DB_FILE):
        return set()
    with open(DB_FILE, "r") as file:
        return set(line.strip() for line in file if line.strip())

def save_uid(uid):
    uids = load_registered_uids()
    if uid not in uids:
        with open(DB_FILE, "a") as file:
            file.write(f"{uid}\n")
        return True
    return False

def remove_uid(uid):
    uids = load_registered_uids()
    if uid in uids:
        uids.remove(uid)
        with open(DB_FILE, "w") as file:
            for u in uids:
                file.write(f"{u}\n")
        return True
    return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    welcome_text = (
        f"👋 Hello {user_name}!\n\n"
        f"Welcome to the **JAGUAR COLOUR TRADING VIP Verification Bot**.\n\n"
        f"📌 **Step 1:** हमारे पार्टनर लिंक से Exness अकाउंट बनाएं:\n"
        f"👉 [Click Here to Sign Up](https://exnessonelink.com)\n"
        f"➡️ Partner Code: `bot68`\n\n"
        f"📌 **Step 2:** अकाउंट बनाने के बाद, अपना **Exness Account Number (UID)** यहाँ चैट में टाइप करके भेजें।"
    )
    keyboard = [[InlineKeyboardButton("📈 Open Exness Account", url="https://exnessonelink.com")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown", disable_web_page_preview=True)

async def add_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if not context.args:
        await update.message.reply_text("❌ फॉर्मेट: `/add [Account_Number]`", parse_mode="Markdown")
        return
    uid = context.args[0].strip()
    if save_uid(uid):
        await update.message.reply_text(f"✅ Account `{uid}` को सफलतापूर्वक लिस्ट में जोड़ दिया गया है।", parse_mode="Markdown")
    else:
        await update.message.reply_text(f"ℹ️ Account `{uid}` पहले से ही मौजूद है।", parse_mode="Markdown")

async def del_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if not context.args:
        await update.message.reply_text("❌ फॉर्मेट: `/del [Account_Number]`", parse_mode="Markdown")
        return
    uid = context.args[0].strip()
    if remove_uid(uid):
        await update.message.reply_text(f"🗑️ Account `{uid}` को लिस्ट से हटा दिया गया है।", parse_mode="Markdown")
    else:
        await update.message.reply_text(f"❌ Account `{uid}` लिस्ट में नहीं मिला।", parse_mode="Markdown")

async def verify_uid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    if not user_input.isdigit():
        await update.message.reply_text("❌ कृपया केवल अंकों में अपना सही Exness Account Number (UID) भेजें।")
        return
    registered_uids = load_registered_uids()
    if user_input in registered_uids:
        success_keyboard = [[InlineKeyboardButton("💬 Join VIP Group", url=VIP_GROUP_LINK)]]
        markup = InlineKeyboardMarkup(success_keyboard)
        await update.message.reply_text(
            f"✅ **Verification Successful!**\n\n"
            f"आपका अकाउंट नंबर ({user_input}) वेरिफाई हो गया है।\n"
            f"नीचे दिए गए बटन पर क्लिक करके VIP Group जॉइन करें 👇",
            reply_markup=markup,
            parse_mode="Markdown"
        )
    else:
        fail_text = (
            f"❌ **Verification Failed!**\n\n"
            f"अकाउंट नंबर `{user_input}` हमारे पार्टनर डेटाबेस में नहीं मिला।\n\n"
            f"💡 **क्या करें?**\n"
            f"1. पक्का करें कि आपने [हमारे लिंक](https://exnessonelink.com) से ही अकाउंट बनाया है।\n"
            f"2. अगर अभी बनाया है, तो हमारे पास लिस्ट अपडेट होने में थोड़ा समय लग सकता है।"
        )
        await update.message.reply_text(fail_text, parse_mode="Markdown", disable_web_page_preview=True)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add_user))
    app.add_handler(CommandHandler("del", del_user))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, verify_uid))
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
