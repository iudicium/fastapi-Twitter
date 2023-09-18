from typing import Dict
from random import randint
import pytest
from httpx import AsyncClient
from faker import Faker

from src.models.tweets import Tweet
from src.tests.conftest import client


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
        data = response.json()
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
            == "Regrettably, Your Entry Has Been Met With an Imposing Barrier, Rendering Further Passage Unattainable"
        )
        assert data["result"] == False

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
        print(self.expected_response, 123)
        url = self.likes_url.format("2")
        response = await client.delete(url)

        assert response.status_code == 404
        assert response.json() == self.error_response
