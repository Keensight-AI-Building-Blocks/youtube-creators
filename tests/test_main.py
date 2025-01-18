from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_load_data():
    response = client.post("/load", json={"video_id": "vddu2jmfVbI"})
    assert (
        response.status_code == 200
    ), f"Expected status code 200, but got {response.status_code}. Response: {response.text}"


def test_query():
    response = client.post("/query", json={"query": "some_query", "chat_history": []})
    assert (
        response.status_code == 200
    ), f"Expected status code 200, but got {response.status_code}. Response: {response.text}"
    assert (
        "answer" in response.json()
    ), f"'answer' not in response. Response: {response.json()}"


def test_health_check():
    response = client.get("/health")
    assert (
        response.status_code == 200
    ), f"Expected status code 200, but got {response.status_code}. Response: {response.text}"
    json_response = response.json()
    assert (
        json_response["status"] == "healthy"
    ), f"Expected status 'healthy', but got {json_response['status']}. Response: {json_response}"
    assert (
        "uptime" in json_response
    ), f"'uptime' not in response. Response: {json_response}"
    assert (
        "current_time" in json_response
    ), f"'current_time' not in response. Response: {json_response}"


def test_metadata():
    response = client.get("/metadata")
    assert (
        response.status_code == 200
    ), f"Expected status code 200, but got {response.status_code}. Response: {response.text}"
    json_response = response.json()
    assert (
        "Debug" in json_response
    ), f"'Debug' not in response. Response: {json_response}"
    assert (
        "Frontend_Origins" in json_response
    ), f"'Frontend_Origins' not in response. Response: {json_response}"
    assert (
        "OPENAI_API_Key_Set" in json_response
    ), f"'OPENAI_API_Key_Set' not in response. Response: {json_response}"
    assert (
        "Model_Name" in json_response
    ), f"'Model_Name' not in response. Response: {json_response}"
    assert (
        "Base_URL" in json_response
    ), f"'Base_URL' not in response. Response: {json_response}"
    assert (
        "YOUTUBE_API_Key_Set" in json_response
    ), f"'YOUTUBE_API_Key_Set' not in response. Response: {json_response}"


def test_get_comments():
    response = client.post("/get_comments", json={"video_id": "vddu2jmfVbI"})
    assert (
        response.status_code == 200
    ), f"Expected status code 200, but got {response.status_code}. Response: {response.text}"
    json_response = response.json()
    assert (
        "Comments" in json_response
    ), f"'Comments' not in response. Response: {json_response}"


def test_get_trending_videos():
    response = client.post("/get_trending_videos", json={"category_id": 24})
    assert (
        response.status_code == 200
    ), f"Expected status code 200, but got {response.status_code}. Response: {response.text}"
    json_response = response.json()
    assert (
        "Videos" in json_response
    ), f"'Videos' not in response. Response: {json_response}"


def test_set_env_vars():
    response = client.post("/set_env_vars", json={"vars": {"TEST_KEY": "TEST_VALUE"}})
    assert (
        response.status_code == 200
    ), f"Expected status code 200, but got {response.status_code}. Response: {response.text}"
    json_response = response.json()
    assert (
        json_response["status"] == "success"
    ), f"Expected status 'success', but got {json_response['status']}. Response: {json_response}"
