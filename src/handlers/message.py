import logging
from src.bot_instance import bot, logged_message_handler

logger = logging.getLogger(__name__)

@logged_message_handler(func=lambda message: True)
async def echo_message(message):
    try:
        if message.text:  # Only handle text messages
            logger.info(f"Processing echo message from user {message.from_user.id}")
            await bot.reply_to(message, f"You said: {message.text}")
            logger.info("Echo message processed successfully")
        else:
            logger.info(f"Processing non-text message from user {message.from_user.id}")
            await bot.reply_to(message, "I can only echo text messages!")
    except Exception as e:
        logger.error(f"Error in echo_message: {e}", exc_info=True)
        try:
            await bot.reply_to(message, "Sorry, something went wrong. Please try again.")
        except Exception as reply_error:
            logger.error(f"Failed to send error message: {reply_error}")
