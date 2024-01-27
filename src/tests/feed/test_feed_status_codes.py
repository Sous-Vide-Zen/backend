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
def test_feed(api_client):
    url = "http://127.0.0.1:8000/api/v1/feed/"
    response = api_client.get(url)
    assert response.status_code == 200


# @pytest.mark.feed
# @pytest.mark.api
# def test_feed_subscriptions_unauth(api_client):
#     """
#     Should be 401, available only for authorized users
#     """
#     client = APIClient()
#     url = "http://127.0.0.1:8000/api/v1/feed/?filter=subscriptions"
#     response = client.get(url)
#     assert response.status_code == 401
#
#
# @pytest.mark.feed
# @pytest.mark.api
# @pytest.mark.django_db
# def test_feed_subscriptions_auth():
#     """
#     Should be 401, available only for authorized users
#     """
#     client = APIClient()
#     client.force_authenticate()
#     url = "http://127.0.0.1:8000/api/v1/feed/?filter=subscriptions"
#     response = client.get(url)
#     assert response.status_code == 401
