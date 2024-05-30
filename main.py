import os 
import logging
from groq import Groq
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

GROQ_API_KEY = os.getenv('GROQ_API_KEY', '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')
GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama3-70b-8192')

client = Groq(
    api_key=GROQ_API_KEY
)

messages = []
def groq_response(text: str) -> str:
    messages.append({
        "role": "user",
        "content": text
    })
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=GROQ_MODEL,
        stream=False,
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stop=None,
    )
    response = chat_completion.choices[0].message.content
    messages.append({
        "role": "assistant",
        "content": response
    })
    return response

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN', '6913989333:AAE4RkixHTHVQ7OLBvQW_6horzVzXH2IKmo')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    messages.append({
        "role": "system",
        "content": f"Anda adalah AI yang sangat cerdas dan berpengetahuan luas seperti ChatGPT, dengan nama YumAI. Anda selalu menjawab pertanyaan dan memberikan informasi dalam bahasa Indonesia dengan gaya yang ramah dan profesional."
    })
    await update.message.reply_html(
        rf"Halo YumAI! Saya siap membantu Anda.",
        reply_markup=ForceReply(selective=True),
    )

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /reset is issued."""
    user = update.effective_user
    messages.clear()
    await start(update, context)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(groq_response(update.message.text))

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main() -> None:
    """Start the bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("reset", reset))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_error_handler(error)

    application.run_polling()

if __name__ == "__main__":
    main()
