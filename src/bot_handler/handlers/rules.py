import logging
from src.bot_handler.bot_instance import bot, logged_message_handler

logger = logging.getLogger(__name__)

@logged_message_handler(commands=['rules'])
async def send_rules(message):
    try:
        logger.info(f"Processing rules command from user {message.from_user.id}")
        text = 'Bot rules:\n1. Be respectful\n2. No spam\n3. Have fun!'
        await bot.reply_to(message, text)
        logger.info("Rules command processed successfully")
    except Exception as e:
        logger.error(f"Error in send_rules: {e}", exc_info=True)
        try:
            await bot.reply_to(message, "Sorry, something went wrong. Please try again.")
        except Exception as reply_error:
            logger.error(f"Failed to send error message: {reply_error}")
