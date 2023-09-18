from io import BytesIO
from os import listdir
from pathlib import Path
from shutil import rmtree

import pytest
from httpx import AsyncClient

from src.tests.conftest import TEST_USERNAME
from src.utils.settings import MEDIA_PATH


@pytest.fixture(scope="class")
def temp_media_dir(request):
    """Clean up of folder media"""
    test_user_media_path = MEDIA_PATH / TEST_USERNAME
    Path(test_user_media_path).mkdir(parents=True, exist_ok=True)
    yield test_user_media_path
    rmtree(test_user_media_path)


class TestMediaAPI:
    @classmethod
    def setup_class(cls):
        image_content = b"test"
        image_file = BytesIO(image_content)
        cls.files = {"file": ("image.jpg", image_file)}
        cls.invalid_files = {"file": ("image.jpg")}
        cls.base_url = "/medias"
        cls.test_user_media_path = MEDIA_PATH / TEST_USERNAME

    @pytest.mark.asyncio
    async def test_media_route(self, client: AsyncClient, temp_media_dir):
        response = await client.post(self.base_url, files=self.files)

        assert response.status_code == 201
        assert response.json() == {"result": True, "media_id": 1}
        files = listdir(self.test_user_media_path)
        if len(files) >= 1:
            hash, file_extension = files[0].split(".")
            assert len(hash) == 64
            assert file_extension == "jpg"

    @pytest.mark.asyncio
    async def test_incorrect_api_key(self, client: AsyncClient):
        headers = {"api_key": "RMTREE"}
        response = await client.post(self.base_url, headers=headers, files=self.files)
        assert response.status_code == 401
