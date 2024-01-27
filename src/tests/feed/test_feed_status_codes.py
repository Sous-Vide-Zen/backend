import pytest
from rest_framework.test import APIClient

"""
http://127.0.0.1:8000/api/v1/feed/?ordering=-activity_count"
"http://127.0.0.1:8000/api/v1/feed/"
"http://127.0.0.1:8000/api/v1/feed/?filter=subscriptions"
"""


@pytest.mark.feed
@pytest.mark.api
@pytest.mark.django_db
class TestFeedCodes:
    def test_feed(self, api_client):
        url = "/api/v1/feed/"
        response = api_client.get(url)
        assert response.status_code == 200

    def test_feed_subscriptions_unauth(self, api_client):
        """
        Should be 401, available only for authorized users
        """
        client = APIClient()
        url = "/api/v1/feed/?filter=subscriptions"
        response = client.get(url)
        assert response.status_code == 401

    def test_feed_subscriptions_auth(self, api_client, create_token):
        """
        Should be 200 after getting token
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=create_token)
        url = "/api/v1/feed/?filter=subscriptions"
        response = client.get(url)
        assert response.status_code == 200
