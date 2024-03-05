import pytest

"""
http://127.0.0.1:8000/api/v1/feed/?ordering=-activity_count"
"http://127.0.0.1:8000/api/v1/feed/"
"http://127.0.0.1:8000/api/v1/feed/?filter=subscriptions"
"""


@pytest.mark.feed
@pytest.mark.api
@pytest.mark.django_db
class TestFeedCodes:
    """
    Feed status codes test
    """

    def test_feed(self, api_client):
        """
        Should be 200
        """

        url = "/api/v1/feed/"
        response = api_client.get(url)
        assert response.status_code == 200

    def test_feed_subscriptions_unauth(self, api_client):
        """
        Should be 401, available only for authorized users
        """

        url = "/api/v1/feed/?filter=subscriptions"
        response = api_client.get(url)
        assert response.status_code == 401

    def test_feed_subscriptions_auth(self, api_client, create_token):
        """
        Should be 401 for unauthorized user and 200 after getting token
        """

        url = "/api/v1/feed/?filter=subscriptions"
        response_guest = api_client.get(url)
        assert response_guest.status_code == 401

        api_client.credentials(HTTP_AUTHORIZATION=create_token)
        response_authorized = api_client.get(url)
        assert response_authorized.status_code == 200
