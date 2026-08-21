import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app
from app.services.x_api import XAPIError

client = TestClient(app)

@patch("app.services.x_api._make_request")
@patch("app.routes.analysis.predict_risk")
@patch("app.routes.analysis.explain_risk")
def test_valid_username_analysis(mock_explain, mock_predict, mock_request, mock_x_user, mock_x_posts):
    # Setup mocks
    mock_request.side_effect = [mock_x_user, mock_x_posts]
    mock_predict.return_value = ({"score": 30, "probability": 0.3, "level": "moderate"}, ["Some signal"])
    mock_explain.return_value = "This is a mocked explanation."
    
    response = client.post("/api/analyze", json={"username": "testuser"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["account"]["username"] == "testuser"
    assert data["risk"]["score"] == 30
    assert data["explanation"] == "This is a mocked explanation."
    assert "account_age_days" in data["features"]

@patch("app.services.x_api._make_request")
def test_invalid_username_404(mock_request):
    mock_request.side_effect = XAPIError("Resource not found on X", 404)
    response = client.post("/api/analyze", json={"username": "unknown_user"})
    assert response.status_code == 404

@patch("app.services.x_api._make_request")
def test_x_api_401(mock_request):
    mock_request.side_effect = XAPIError("Unauthorized", 401)
    response = client.post("/api/analyze", json={"username": "testuser"})
    assert response.status_code == 401

@patch("app.services.x_api._make_request")
def test_x_api_429(mock_request):
    mock_request.side_effect = XAPIError("Rate limit exceeded", 429)
    response = client.post("/api/analyze", json={"username": "testuser"})
    assert response.status_code == 429

@patch("app.services.x_api._make_request")
@patch("app.routes.analysis.predict_risk")
def test_empty_post_list(mock_predict, mock_request, mock_x_user):
    mock_request.side_effect = [mock_x_user, {"data": []}]
    mock_predict.return_value = ({"score": 10, "probability": 0.1, "level": "low"}, [])
    
    response = client.post("/api/analyze", json={"username": "testuser"})
    assert response.status_code == 200
    assert response.json()["account"]["posts"] == 2000

@patch("app.services.x_api._make_request")
@patch("app.routes.analysis.predict_risk")
def test_zero_following_and_followers(mock_predict, mock_request, mock_x_user, mock_x_posts):
    mock_x_user["data"]["public_metrics"]["followers_count"] = 0
    mock_x_user["data"]["public_metrics"]["following_count"] = 0
    mock_request.side_effect = [mock_x_user, mock_x_posts]
    mock_predict.return_value = ({"score": 90, "probability": 0.9, "level": "high"}, ["Zero followers"])
    
    response = client.post("/api/analyze", json={"username": "testuser"})
    assert response.status_code == 200
    assert response.json()["features"]["followers_following_ratio"] == 0.0

@patch("app.services.x_api._make_request")
@patch("app.routes.analysis.predict_risk")
def test_missing_metrics(mock_predict, mock_request, mock_x_user, mock_x_posts):
    del mock_x_posts["data"][0]["public_metrics"]
    mock_request.side_effect = [mock_x_user, mock_x_posts]
    mock_predict.return_value = ({"score": 50, "probability": 0.5, "level": "moderate"}, [])
    
    response = client.post("/api/analyze", json={"username": "testuser"})
    assert response.status_code == 200
    assert response.json()["features"]["average_likes"] >= 0

@patch("app.services.x_api._make_request")
def test_ml_model_loading_failure(mock_request, mock_x_user, mock_x_posts):
    mock_request.side_effect = [mock_x_user, mock_x_posts]
    # To simulate ML failure, we patch predict_risk to raise RuntimeError
    with patch("app.routes.analysis.predict_risk", side_effect=RuntimeError("ML Model not loaded")):
        response = client.post("/api/analyze", json={"username": "testuser"})
        assert response.status_code == 503

@patch("app.services.x_api._make_request")
@patch("app.routes.analysis.extract_features")
def test_feature_schema_mismatch(mock_extract, mock_request, mock_x_user, mock_x_posts):
    mock_request.side_effect = [mock_x_user, mock_x_posts]
    mock_extract.return_value = {"missing_expected_feature": 1} # Invalid schema
    
    response = client.post("/api/analyze", json={"username": "testuser"})
    assert response.status_code == 500

@patch("app.services.x_api._make_request")
@patch("app.routes.analysis.predict_risk")
@patch("app.routes.analysis.explain_risk")
def test_gemini_failure_still_returns_ml_result(mock_explain, mock_predict, mock_request, mock_x_user, mock_x_posts):
    mock_request.side_effect = [mock_x_user, mock_x_posts]
    mock_predict.return_value = ({"score": 30, "probability": 0.3, "level": "moderate"}, [])
    mock_explain.return_value = None # Simulate Gemini failure/timeout
    
    response = client.post("/api/analyze", json={"username": "testuser"})
    assert response.status_code == 200
    assert response.json()["explanation"] is None
    assert response.json()["risk"]["score"] == 30
