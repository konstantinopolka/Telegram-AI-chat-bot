import logging
from src.bot_instance import bot, logged_message_handler
from src.dao.models import User, AsyncSessionLocal


logger = logging.getLogger(__name__)

@logged_message_handler(commands=['help', 'start'])
async def send_welcome(message):
    try:
        async with AsyncSessionLocal() as session:
            logger.info(f"Processing welcome command from user {message.from_user.id}")
            user = await session.get(User, message.from_user.id)
            if not user:
                user = User(
                    telegram_id=message.from_user.id,
                    username=message.from_user.username,
                    first_name=message.from_user.first_name,
                    last_name=message.from_user.last_name,
                )
                session.add(user)
                await session.commit()
                await bot.reply_to(message, "Welcome, you have been registered!")
                logger.info("New user registered and welcomed.")
            else:
                await bot.reply_to(message, f"Welcome back, {message.from_user.username}")
                logger.info("Returning user welcomed.")
    except Exception as e:
        logger.error(f"Error in send_welcome: {e}", exc_info=True)
        try:
            await bot.reply_to(message, "Sorry, something went wrong. Please try again.")
        except Exception as reply_error:
            logger.error(f"Failed to send error message: {reply_error}")
