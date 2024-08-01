import logging

from aiogram import Bot

logger = logging.getLogger(__name__)


async def update_progress(
    bot: Bot,
    progress_text: str,
    chat_id: int | str | None,
    message_id: int | None,
) -> None:
    """
    Updates the progress message in a specified chat.

    Args:
        bot (Bot): An instance of the Bot to perform the message update.
        progress_text (str): The text to update the message with.
        chat_id (int | str | None): The ID of the chat where
        the message is located.
        message_id (int | None): The ID of the message to be updated.
    """
    logger.info(f"Updating progress: {progress_text}")
    await bot.edit_message_text(
        progress_text, chat_id=chat_id, message_id=message_id
    )
