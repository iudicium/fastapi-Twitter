from os.path import splitext
from aiofiles import open
from hashlib import sha256
from fastapi import UploadFile
from src.utils.settings import MEDIA_PATH


async def generate_hash_from_filename(file_name: str) -> str:
    """
    Generates a unique hash-based file name from the given file name.

    :param file_name: The original file name to be hashed.
    :return: A unique hash-based file name including the original file extension.
    """
    name, extension = splitext(file_name)
    hash_object = sha256(name.encode())
    hashed_name = hash_object.hexdigest()
    return f"{hashed_name}{extension}"


async def save_uploaded_file(user_name: str, uploaded_file: UploadFile) -> str:
    """
    Uploads a file to the user's directory and returns the relative path for improved security.
    :param user_name: The username of the user who is uploading the file.
    :param uploaded_file: The FastAPI UploadFile object representing the uploaded file.
    :return: The relative path to the saved file.
    :raises: Any exceptions that may occur during file upload and storage.
    """

    user_dir = MEDIA_PATH / user_name
    user_dir.mkdir(parents=True, exist_ok=True)

    unique_filename = await generate_hash_from_filename(uploaded_file.filename)

    file_path = user_dir / unique_filename
    content = uploaded_file.file.read()
    async with open(file_path, "wb") as file:
        await file.write(content)

    relative_path = str(file_path.relative_to(MEDIA_PATH))
    return relative_path
