import os
import pytest
from fastapi.testclient import TestClient
from main import app
from app.services.trie_manager import TrieManager

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/prefixes.json")


# Manually initialize Trie for tests
def setup_trie():
    TrieManager.initialize_trie()


@pytest.fixture(scope="module", autouse=True)
def initialize_trie():
    """Fixture to ensure Trie is loaded before tests."""
    setup_trie()


# Create TestClient AFTER Trie is initialized
client = TestClient(app)

# Test Valid Single IP Lookup
def test_lookup_single_ip_found():
    """Test single IP lookup where IP exists in Trie"""
    response = client.get("/api/v1/lookup/184.51.33.230")
    assert response.status_code == 200, f"Unexpected response: {response.json()}"
    assert "result" in response.json()


# Test Invalid Single IP Lookup (422 Validation Error)
def test_lookup_single_ip_invalid():
    """Test single IP lookup with an invalid IP format"""
    response = client.get("/api/v1/lookup/999.999.999.999")  # Invalid IP
    assert response.status_code == 422


# Test Single IP Not Found (404)
def test_lookup_single_ip_not_found():
    """Test single IP lookup where IP is not in Trie"""
    response = client.get("/api/v1/lookup/8.8.8.8")
    assert response.status_code == 404
    assert response.json()["detail"] == "IP not found in any subnet"


# Test Valid Batch Lookup
def test_lookup_batch():
    """Test batch lookup for multiple valid IPs"""
    request_data = {"ips": ["184.51.33.230", "23.79.232.100"]}
    response = client.post("/api/v1/lookup/batch", json=request_data)
    assert response.status_code == 200
    assert "result" in response.json()


# Test Batch Lookup with No Matching IPs (404)
def test_lookup_batch_no_results():
    """Test batch lookup where no IPs are found in Trie"""
    request_data = {"ips": ["8.8.8.8", "1.2.3.4"]}
    response = client.post("/api/v1/lookup/batch", json=request_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "No IPs found in any subnet"


# Test Batch Lookup with Mixed Valid and Invalid IPs
def test_lookup_batch_mixed():
    """Test batch lookup with both valid and invalid IPs"""
    request_data = {"ips": ["184.51.33.230", "invalid-ip"]}
    response = client.post("/api/v1/lookup/batch", json=request_data)
    assert response.status_code == 422  # Should fail due to invalid IP


# Test Batch Lookup with Empty List (422)
def test_lookup_batch_empty_list():
    """Test batch lookup with an empty list"""
    request_data = {"ips": []}
    response = client.post("/api/v1/lookup/batch", json=request_data)
    assert response.status_code == 422  # Validation should fail


# Test Batch Lookup with IPv6 Addresses
def test_lookup_batch_ipv6():
    """Test batch lookup with IPv6 addresses"""
    request_data = {"ips": ["2001:db8::ff00:42", "2a00:1450:4009:80b::200e"]}
    response = client.post("/api/v1/lookup/batch", json=request_data)
    assert response.status_code in [200, 404]  # Should be 200 if IPv6 exists, else 404
