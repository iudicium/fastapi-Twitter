from pathlib import Path
from aiofiles import open
from fastapi import UploadFile

from src.utils.settings import MEDIA_PATH


async def check_or_get_filename(path: Path) -> Path:
    """
    Adds a numerical suffix to the filename if a file with the same name already exists.
    :param path: The path to check and modify.
    :return: The modified path with a numerical suffix.
    """
    original_path = path
    counter = 0

    while path.exists():
        counter += 1
        filename = f"{original_path.stem} ({counter}){original_path.suffix}"
        path = original_path.with_name(filename)
    print(path)
    return path


async def save_uploaded_file(uploaded_file: UploadFile) -> str:
    """
    Uploads a file and returns the relative path
    :param uploaded_file: The FastAPI UploadFile object representing the uploaded file.
    :return: The relative path to the saved file.
    :raises: Any exceptions that may occur during file upload and storage.
    """

    MEDIA_PATH.mkdir(parents=True, exist_ok=True)

    file_path = MEDIA_PATH / uploaded_file.filename
    filename = await check_or_get_filename(path=file_path)
    img_path = f"images/{filename.stem}{filename.suffix}"
    content = uploaded_file.file.read()
    async with open(filename, "wb") as file:
        await file.write(content)
    print(img_path)
    return img_path
