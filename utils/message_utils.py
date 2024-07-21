import logging

from aiogram import Bot

logger = logging.getLogger(__name__)


async def update_progress(
    bot: Bot,
    progress_text: str,
    chat_id: int | str | None,
    message_id: int | None,
):
    logger.info(f"Updating progress: {progress_text}")
    await bot.edit_message_text(
        progress_text, chat_id=chat_id, message_id=message_id
    )
