import logging
from telegram import Update
from telegram.ext import ContextTypes

from database import get_course_names
from scraper import create_course, get_course_details

logger = logging.getLogger(__name__)

async def create_new_course(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat is None:
        logger.warning("Can find effective_chat.id")
        return
    if update.message is None or update.message.text is None:
        logger.warning("Can find message")
        return
    
    course_id = update.message.text.split('/new_course')[1]
    create_course(int(course_id))
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Created new course for id {course_id}")

async def get_course_with_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat is None:
        logger.warning("Can find effective_chat.id")
        return
    if update.message is None or update.message.text is None:
        logger.warning("Can find message")
        return
    
    course_name = update.message.text.split('/course ')[1]
    if course_name == '' or course_name == ' ':
        logger.warning("Message doesn't contain course name")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Message doesn't contain course name")
        return

    upcoming_tournaments = get_course_details(course_name)
    tournament_str = ''
    for tournament in upcoming_tournaments:
        tournament_str += f'{tournament[1]} - {tournament[0]}\n'
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Upcoming tournaments for course: {course_name} \n{tournament_str}")

async def list_courses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat is None:
        logger.warning("Can find effective_chat.id")
        return
    if update.message is None or update.message.text is None:
        logger.warning("Can find message")
        return
    
    course_names = get_course_names()
    course_str = ''
    for course in course_names:
        course_str += f'{course[0]}\n'
        
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Available courses: \n{course_str}')