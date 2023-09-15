import pytest
from _pytest._py.path import LocalPath

from src.tests.conftest import client
from httpx import AsyncClient
from io import BytesIO
from src.utils.settings import MEDIA_PATH


class TestMediaAPI:
    @pytest.mark.asyncio
    async def test_media_route(self, tmpdir: LocalPath, client: AsyncClient):
        image_content = b"test"
        image_file = BytesIO(image_content)

        files = {"file": ("image.jpg", image_file)}

        response = await client.post("/medias", files=files)

        assert response.status_code == 201
        assert response.json() == {"result": True, "media_id": 1}
        print(MEDIA_PATH)
