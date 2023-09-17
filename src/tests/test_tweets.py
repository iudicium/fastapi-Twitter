from typing import Dict
import pytest
from httpx import AsyncClient
from faker import Faker
from sqlalchemy import text

from src.tests.conftest import client


async def create_random_tweet(client: AsyncClient, json: Dict, tweet_data: str):
    json["tweet_data"] = tweet_data
    await client.post("/tweets", json=json)


class TestTweetAPI:
    @classmethod
    def setup_class(cls):
        cls.faker = Faker()
        cls.base_url = "/tweets"
        cls.tweet_structure = {
            "tweet_data": "",
            "tweet_media_ids": [],
        }
        cls.expected_response = {"result": True, "tweet_id": 1}

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
        assert "false" in response.json()

    @pytest.mark.asyncio
    async def test_delete_tweet(self, client: AsyncClient):
        url = f"{self.base_url}/1"
        response = await client.delete(url)
        assert response.status_code == 200
        assert response.json() == {"result": True}

    # TODO test unauthorized tweet deletion
