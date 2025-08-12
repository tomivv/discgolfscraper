import logging
from dotenv import dotenv_values
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from bot.commands import create_new_course, get_course_with_name, list_courses

secrets = dotenv_values(".env.local")
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat is not None:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    else:
        logger.warning("No effective_chat found in update.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat is not None and update.message is not None and update.message.text is not None:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def run_bot():
    bot_key = secrets['TGBOT_KEY']
    if bot_key is None:
        logger.critical('Failed to start bot: Unable to load key')
        return
    application = ApplicationBuilder().token(bot_key).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(CommandHandler('new_course', create_new_course))
    application.add_handler(CommandHandler('course', get_course_with_name))
    application.add_handler(CommandHandler('list_courses', list_courses))
    
    application.run_polling()

if __name__ == '__main__':
    run_bot()