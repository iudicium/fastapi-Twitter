import os
import asyncio
import aiofiles

from src.utils.settings import MEDIA_PATH


async def save_uploaded_file(user_id, uploaded_file):
    user_dir = os.path.join("media", f"user_{user_id}")
    unique_filename = generate_unique_filename(uploaded_file.filename)

    async with aiofiles.open(os.path.join(user_dir, unique_filename), "wb") as f:
        await f.write(uploaded_file.file.read())
