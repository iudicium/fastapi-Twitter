from random import randint
import pytest
from httpx import AsyncClient
from src.tests.conftest import client


class TestMediaAPI:
    @classmethod
    def setup_class(cls):
        cls.base_url = "/users/{}/follow"
        cls.expected_response = {"result": True}
        cls.bad_response = {"detail": "You are not following this user."}

    @pytest.mark.asyncio
    async def test_follow_user_correct(self, client: AsyncClient):
        response = await client.post(self.base_url.format("2"))
        assert response.status_code == 201
        assert response.json() == self.expected_response

    @pytest.mark.asyncio
    async def test_follow_yourself(self, client: AsyncClient):
        response = await client.post(self.base_url.format("1"))
        data = response.json()
        assert response.status_code == 400
        assert "Unable to follow yourself" in data

    @pytest.mark.asyncio
    async def test_follow_user_that_doesnt_exist(self, client: AsyncClient):
        response = await client.post(self.base_url.format("10000"))
        assert response.status_code == 404
        assert "User does not exist" in response.json()

    @pytest.mark.asyncio
    async def test_unfollow_user(self, client: AsyncClient):
        url = self.base_url.format("5")
        following_response = await client.post(url)
        assert following_response.status_code == 201
        unfollow_response = await client.delete(url)
        assert unfollow_response.status_code == 200
        assert unfollow_response.json() == self.expected_response

    @pytest.mark.asyncio
    async def test_unfollow_user_that_is_not_followed(self, client: AsyncClient):
        response = await client.delete(self.base_url.format(6))
        assert response.status_code == 400
        assert "You are not following this user" in response.json()

    @pytest.mark.asyncio
    async def test_get_user_information(self, client: AsyncClient):
        url = self.base_url.replace("/follow", "")
        response = await client.get(url.format(1))
        data = response.json()
        assert response.status_code == 200
        assert data["result"] == True

    @pytest.mark.asyncio
    async def test_get_me_information(self, client: AsyncClient):
        url = self.base_url.replace("{}/follow", "me")
        response = await client.get(url)
        data = response.json()
        assert response.status_code == 200
        assert data["result"] == True
