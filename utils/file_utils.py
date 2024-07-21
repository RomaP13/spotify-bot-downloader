import os
import zipfile

from aiogram import types


def create_zip_file(directory: str, zip_path: str) -> None:
    """
    Create a ZIP file containing all .mp3 files in a specified directory.

    Args:
        directory (str): The directory containing .mp3 files to be zipped.
        zip_path (str): The path where the ZIP file will be created.
    """
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for file in os.listdir(directory):
            if file.endswith(".mp3"):
                zipf.write(
                    os.path.join(directory, file),
                    os.path.join(os.path.basename(directory), file),
                )


async def send_file_to_user(
    message: types.Message, file_path: str, file_type: str
) -> None:
    """
    Send a file to the user via Telegram.

    Args:
        message (types.Message): The Telegram message object.
        file_path (str): The path to the file to be sent.
        file_type (str): The type of the file, either 'audio' or 'document'.

    Raises:
        ValueError: If the file_type is not 'audio' or 'document'.
    """
    if file_type == "audio":
        file = types.FSInputFile(file_path)
        await message.answer_audio(file)
    elif file_type == "document":
        file = types.FSInputFile(file_path)
        await message.answer_document(file)
    else:
        raise ValueError("Unsupported file type. Use 'audio' or 'document'.")
