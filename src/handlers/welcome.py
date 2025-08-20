import logging
from src.bot_instance import bot, logged_message_handler

logger = logging.getLogger(__name__)

@logged_message_handler(commands=['help', 'start'])
async def send_welcome(message):
    try:
        logger.info(f"Processing welcome command from user {message.from_user.id}")
        text = 'Hi, I am ServeBot.\nJust write me something and I will repeat it!'
        await bot.reply_to(message, text)
        logger.info("Welcome command processed successfully")
    except Exception as e:
        logger.error(f"Error in send_welcome: {e}", exc_info=True)
        try:
            await bot.reply_to(message, "Sorry, something went wrong. Please try again.")
        except Exception as reply_error:
            logger.error(f"Failed to send error message: {reply_error}")
