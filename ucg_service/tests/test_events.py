import uuid
from http import HTTPStatus

from flask_jwt_extended import create_access_token


def test_click_event(app):
    with app.app_context():
        client = app.test_client()
        access_token = create_access_token(identity="user")
        headers = {"Authorization": "Bearer " + access_token}
        response = client.post(
            "/api/v1/events/clicks",
            json={"type": "film"},
            headers=headers,
        )
        assert response.status_code == HTTPStatus.OK


def test_unauthorized_click_event(app):
    with app.app_context():
        client = app.test_client()
        response = client.post(
            "/api/v1/events/clicks",
            json={"type": "film"},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_seen_pages(app):
    with app.app_context():
        client = app.test_client()
        access_token = create_access_token(identity="user")
        headers = {"Authorization": "Bearer " + access_token}
        response = client.post(
            "/api/v1/events/seen-pages",
            json={"url": "http://ya.ru", "duration": 10},
            headers=headers,
        )
        assert response.status_code == HTTPStatus.OK


def test_video_quality(app):
    with app.app_context():
        client = app.test_client()
        access_token = create_access_token(identity="user")
        headers = {"Authorization": "Bearer " + access_token}
        response = client.post(
            "/api/v1/events/video-quality",
            json={"old_quality": "1080p", "new_quality": "720p"},
            headers=headers,
        )
        assert response.status_code == HTTPStatus.OK


def test_film_view(app):
    with app.app_context():
        client = app.test_client()
        access_token = create_access_token(identity="user")
        headers = {"Authorization": "Bearer " + access_token}
        response = client.post(
            "/api/v1/events/film-view",
            json={"film_id": str(uuid.uuid4())},
            headers=headers,
        )
        assert response.status_code == HTTPStatus.OK


def test_filter_by(app):
    with app.app_context():
        client = app.test_client()
        access_token = create_access_token(identity="user")
        headers = {"Authorization": "Bearer " + access_token}
        response = client.post(
            "/api/v1/events/filter",
            json={"filter_by": "test"},
            headers=headers,
        )
        assert response.status_code == HTTPStatus.OK
