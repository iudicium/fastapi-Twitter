from typing import Dict

import pytest
from faker import Faker
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.tests.conftest import (
    unauthorized_structure_response,
    valid_tweet_timeline_structure,
)


async def create_random_tweet(client: AsyncClient, json: Dict, tweet_data: str):
    json["tweet_data"] = tweet_data
    await client.post("/tweets", json=json)


class TestTweetAPI:
    """
    Main test user has the id of 1
    """

    @classmethod
    def setup_class(cls):
        cls.faker = Faker()
        cls.base_url = "/tweets"
        cls.likes_url = "/tweets/{}/likes"
        cls.tweet_structure = {
            "tweet_data": "",
            "tweet_media_ids": [],
        }
        cls.expected_response = {"result": True}
        cls.error_response = {
            "result": False,
            "error_type": "Not Found",
            "error_message": "",
        }

    @pytest.mark.asyncio
    async def test_create_tweet(self, client: AsyncClient):
        self.tweet_structure["tweet_data"] = self.faker.sentence()

        response = await client.post(self.base_url, json=self.tweet_structure)
        assert response.json() == self.tweet_structure
        assert response.status_code == 201

    @pytest.mark.asyncio
    async def test_create_wrong_tweet_schema(self, client: AsyncClient):
        self.tweet_structure.pop("tweet_data")
        response = await client.post(self.base_url, json=self.tweet_structure)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_delete_tweet(self, client: AsyncClient):
        await create_random_tweet(
            client, json=self.tweet_structure, tweet_data=self.faker.sentence()
        )
        url = f"{self.base_url}/1"
        response = await client.delete(url)
        assert response.status_code == 200
        assert response.json() == self.expected_response

    @pytest.mark.asyncio
    async def test_delete_tweet_from_another_user(
        self, client: AsyncClient, db_session, create_random_tweets
    ):
        url = f"{self.base_url}/2"
        response = await client.delete(url)
        data = response.json()
        assert response.status_code == 403
        assert (
            data["error_message"]
            == "Regrettably, Your Entry Has Been Met With an Imposing Barrier, Rendering "
            "Further Passage Unattainable"
        )
        assert data["result"] is not True

    @pytest.mark.asyncio
    async def test_like_a_tweet(self, client: AsyncClient, create_random_tweets):
        url = self.likes_url.format("1")
        response = await client.post(url)
        assert response.status_code == 201
        assert response.json() == self.expected_response

    @pytest.mark.asyncio
    async def test_like_tweet_that_doesnt_exist(self, client: AsyncClient):
        url = self.likes_url.format("0")
        self.error_response["error_message"] = "Tweet was not found!"
        response = await client.post(url)
        assert response.status_code == 404
        assert response.json() == self.error_response

    @pytest.mark.asyncio
    async def test_delete_tweet_like(self, client: AsyncClient):
        await create_random_tweet(
            client, json=self.tweet_structure, tweet_data=self.faker.sentence()
        )
        url = self.likes_url.format("1")
        response = await client.post(url)
        assert response.status_code == 201
        assert response.json() == self.expected_response
        response = await client.delete(url)
        assert response.status_code == 200
        assert response.json() == self.expected_response

    @pytest.mark.asyncio
    async def test_delete_tweet_like_from_different_user(
        self, client: AsyncClient, create_random_tweets
    ):
        self.error_response["error_message"] = "You already do not like that tweet."

        url = self.likes_url.format("2")
        response = await client.delete(url)

        assert response.status_code == 404
        assert response.json() == self.error_response

    @pytest.mark.asyncio
    async def test_get_timeline_of_tweets(
        self, client: AsyncClient, create_random_tweets, db_session: AsyncSession
    ):
        follow_user = await client.post("/users/4/follow")
        assert follow_user.json() == self.expected_response
        assert follow_user.status_code == 201

        await db_session.execute(
            text("""INSERT INTO media(media_path, tweet_id) VALUES ('image.jpg', 3);""")
        )

        await db_session.execute(
            text("INSERT INTO likes(user_id, tweet_id)" "VALUES(1, 3);")
        )
        await db_session.commit()

        response = await client.get(self.base_url)
        assert response.status_code == 200
        assert response.json() == valid_tweet_timeline_structure

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "unauthorized",
        [
            "/tweets",
            "/tweets/4/likes",
        ],
    )
    async def test_post_unauthorized_access(
        self, invalid_client: AsyncClient, unauthorized: str
    ):
        response = await invalid_client.post(unauthorized)
        assert response.status_code == 401
        assert response.json() == unauthorized_structure_response

    @pytest.mark.asyncio
    @pytest.mark.parametrize("unauthorized", ["/tweets/1", "/tweets/2/likes"])
    async def test_delete_wrong_auth(
        self, invalid_client: AsyncClient, unauthorized: str
    ):
        response = await invalid_client.delete(unauthorized)
        assert response.status_code == 401
        assert response.json() == unauthorized_structure_response

    @pytest.mark.asyncio
    async def test_get_wrong_auth(self, invalid_client: AsyncClient):
        response = await invalid_client.get(self.base_url)
        assert response.status_code == 401
        assert response.json() == unauthorized_structure_response
