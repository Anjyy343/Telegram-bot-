import os
import asyncio
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

conversations = {}
user_memory = {}

SYSTEM_PROMPT = """
You are Wingman, a smart, confident, human-like AI assistant.
Be engaging, insightful, and conversational.
"""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user_msg = update.message.text

    if user_id not in conversations:
        conversations[user_id] = model.start_chat(
            history=[{"role": "user", "parts": [SYSTEM_PROMPT]}]
        )

    if user_id not in user_memory:
        user_memory[user_id] = []

    user_memory[user_id].append(user_msg)
    if len(user_memory[user_id]) > 5:
        user_memory[user_id].pop(0)

    chat = conversations[user_id]
    memory_context = "Recent topics: " + ", ".join(user_memory[user_id])

    try:
        prompt = f"{memory_context}\nUser: {user_msg}"
        response = await asyncio.to_thread(chat.send_message, prompt)
        reply = response.text
    except Exception as e:
        reply = f"Error: {str(e)}"

    await update.message.reply_text(reply)

if __name__ == "__main__":
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")

    if not bot_token:
        raise ValueError("TELEGRAM_BOT_TOKEN not set")

    app = ApplicationBuilder().token(bot_token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()
