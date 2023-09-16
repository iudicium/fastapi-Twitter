import pytest
from httpx import AsyncClient
from src.tests.conftest import TEST_USERNAME, client
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from src.models.users import User, FollowingAssociation


class TestMediaAPI:
    @classmethod
    def setup_class(cls):
        cls.base_url = "/users/{}/follow"
        cls.expected_response = {"result": True}

    @pytest.mark.asyncio
    async def test_follow_user_correct(self, client: AsyncClient):
        response = await client.post(self.base_url.format("2"))
        assert response.status_code == 201
        assert response.json() == self.expected_response

    @pytest.mark.asyncio
    async def test_follow_yourself(self, client: AsyncClient):
        response = await client.post(self.base_url.format("1"))
        assert response.json() == {"detail": "Unable to follow yourself"}
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_follow_user_that_doesnt_exist(self, client: AsyncClient):
        response = await client.post(self.base_url.format("10000"))
        assert response.json() == {"detail": "User does not exist"}
        assert response.status_code == 404
