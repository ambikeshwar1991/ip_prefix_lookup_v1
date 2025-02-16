import pytest
from app.models.trie import IPTrie


@pytest.fixture
def trie():
    """Create a new Trie for each test"""
    trie = IPTrie()
    trie.insert("192.168.1.0/24", "TestProvider", ["TestTag"])
    trie.insert("10.0.0.0/8", "PrivateNetwork", ["Internal"])
    return trie


def test_trie_insert(trie):
    """Test Trie insertion of subnets"""
    assert trie.node_count > 1  # Ensure nodes are created
    assert trie.search("192.168.1.5") is not None
    assert trie.search("10.5.5.5") is not None


def test_trie_lookup_found(trie):
    """Test if known IPs are found"""
    result = trie.search("192.168.1.100")
    assert result is not None
    assert len(result) > 0
    print(f"{result=}")
    assert result[0]["provider"] == "TestProvider"


def test_trie_lookup_not_found(trie):
    """Test lookup of an IP not in the Trie"""
    result = trie.search("8.8.8.8")
    assert result is None
