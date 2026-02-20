import sys
import os
import urllib.parse

# ensure tests can import src.app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.app import activities


def test_get_activities(client):
    # Arrange: none
    # Act
    resp = client.get("/activities")
    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_root_redirect(client):
    # Arrange: none
    # Act
    resp = client.get("/", follow_redirects=False)
    # Assert
    assert resp.status_code in (301, 302, 307, 308)
    assert resp.headers.get("location", "").endswith('/static/index.html')


def test_post_signup_success(client):
    # Arrange
    activity = "Chess Club"
    email = "new@student.edu"
    path = f"/activities/{urllib.parse.quote(activity)}/signup"
    assert email not in activities[activity]["participants"]
    # Act
    resp = client.post(path, params={"email": email})
    # Assert
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]
    assert "Signed up" in resp.json()["message"]


def test_post_signup_already_signed(client):
    # Arrange
    activity = "Chess Club"
    existing = activities[activity]["participants"][0]
    path = f"/activities/{urllib.parse.quote(activity)}/signup"
    # Act
    resp = client.post(path, params={"email": existing})
    # Assert
    assert resp.status_code == 400


def test_post_signup_missing_activity(client):
    # Arrange
    activity = "Nonexistent Club"
    path = f"/activities/{urllib.parse.quote(activity)}/signup"
    # Act
    resp = client.post(path, params={"email": "x@x.com"})
    # Assert
    assert resp.status_code == 404


def test_delete_remove_participant_success(client):
    # Arrange
    activity = "Basketball Team"
    email = "alex@mergington.edu"
    path = f"/activities/{urllib.parse.quote(activity)}/participants"
    assert email in activities[activity]["participants"]
    # Act
    resp = client.delete(path, params={"email": email})
    # Assert
    assert resp.status_code == 200
    assert email not in activities[activity]["participants"]


def test_delete_remove_participant_not_registered(client):
    # Arrange
    activity = "Chess Club"
    email = "nobody@mergington.edu"
    path = f"/activities/{urllib.parse.quote(activity)}/participants"
    # Act
    resp = client.delete(path, params={"email": email})
    # Assert
    assert resp.status_code == 404
