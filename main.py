python
‎import os
‎import google.generativeai as genai
‎from telegram import Update
‎from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
‎
‎genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
‎model = genai.GenerativeModel("gemini-1.5-flash")
‎conversations = {}
‎
‎async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
‎    user_id = str(update.effective_user.id)
‎    user_msg = update.message.text
‎
‎    if user_id not in conversations:
‎        conversations[user_id] = model.start_chat(history=[])
‎
‎    chat = conversations[user_id]
‎
‎    try:
‎        response = chat.send_message(user_msg)
‎        reply = response.text
‎    except Exception as e:
‎        reply = "Something went wrong, try again!"
‎
‎    await update.message.reply_text(reply)
‎
‎if __name__ == "__main__":
‎    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
‎    app = ApplicationBuilder().token(bot_token).build()
‎    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
‎    print("Bot is running...")
‎    app.run_polling()
