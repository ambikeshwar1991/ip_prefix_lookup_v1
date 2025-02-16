import pytest
from fastapi.testclient import TestClient
from main import app
from app.services.trie_manager import TrieManager

client = TestClient(app)

def test_reload_prefixes_success(mocker):
    """
    Test case: Ensure `/reload` API successfully reloads the Trie.
    - Mocks `TrieManager.initialize_trie()` to avoid reloading real data.
    - Checks for correct response and status code.
    """
    mocker.patch.object(TrieManager, "initialize_trie", return_value=None)

    response = client.post("/api/v1/reload")

    assert response.status_code == 200
    assert response.json() == {"message": "Trie reloaded successfully"}

def test_reload_prefixes_failure(mocker):
    """
    Test case: Simulate a failure during Trie reload.
    - Mocks `TrieManager.initialize_trie()` to raise an exception.
    - Ensures API handles errors properly.
    """
    mocker.patch.object(TrieManager, "initialize_trie", side_effect=Exception("Mocked Error"))

    response = client.post("/api/v1/reload")

    assert response.status_code == 500
    assert "Error reloading Trie" in response.json()["detail"]
