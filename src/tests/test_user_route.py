import pytest
from httpx import AsyncClient

from src.tests.conftest import unauthorized_structure_response


class TestMediaAPI:
    @classmethod
    def setup_class(cls):
        cls.base_url = "/users/{}/follow"
        cls.expected_response = {"result": True}
        cls.error_response = {
            "result": False,
            "error_type": "Bad Request",
            "error_message": "",
        }

    @pytest.mark.asyncio
    async def test_follow_user_correct(self, client: AsyncClient):
        response = await client.post(self.base_url.format("2"))
        assert response.status_code == 201
        assert response.json() == self.expected_response

    @pytest.mark.asyncio
    async def test_follow_yourself(self, client: AsyncClient):
        self.error_response["error_message"] = "Unable to follow yourself"

        response = await client.post(self.base_url.format("1"))

        assert response.status_code == 400
        assert response.json() == self.error_response

    @pytest.mark.asyncio
    async def test_follow_user_that_doesnt_exist(self, client: AsyncClient):
        self.error_response["error_type"] = "Not Found"
        self.error_response["error_message"] = "User does not exist."

        response = await client.post(self.base_url.format("10000"))
        assert response.status_code == 404
        assert response.json() == self.error_response

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
        self.error_response["error_type"] = "Bad Request"
        self.error_response["error_message"] = "You are not following this user."
        response = await client.delete(self.base_url.format(6))
        assert response.status_code == 400
        assert response.json() == self.error_response

    @pytest.mark.asyncio
    async def test_get_user_information(self, client: AsyncClient):
        url = self.base_url.replace("/follow", "")
        response = await client.get(url.format(1))
        data = response.json()
        assert response.status_code == 200
        assert data["result"] is True

    @pytest.mark.asyncio
    async def test_get_me_information(self, client: AsyncClient):
        url = self.base_url.replace("{}/follow", "me")
        response = await client.get(url)
        data = response.json()
        assert response.status_code == 200
        assert data["result"] is True

    @pytest.mark.asyncio
    @pytest.mark.parametrize("unauthorized", ["/users/me", "/users/2"])
    async def test_get_wrong_auth(self, invalid_client: AsyncClient, unauthorized: str):
        response = await invalid_client.get(unauthorized)
        print(response.json(), response.status_code)
        assert response.status_code == 401
        assert response.json() == unauthorized_structure_response

    @pytest.mark.asyncio
    async def test_post_wrong_auth(self, invalid_client: AsyncClient):
        response = await invalid_client.post(self.base_url.format("1"))
        assert response.status_code == 401
        assert response.json() == unauthorized_structure_response
