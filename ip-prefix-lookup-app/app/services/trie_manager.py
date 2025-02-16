from concurrent.futures import ThreadPoolExecutor
from app.models.trie import IPTrie
from app.services.data_loader import load_prefixes
import threading

class TrieManager:
    """Manages the global Trie for efficient IP prefix lookups."""

    _trie = IPTrie()
    _lock = threading.Lock()
    _executor = ThreadPoolExecutor(max_workers=10)  # Parallel execution for batch lookups

    @classmethod
    def initialize_trie(cls):
        """Initializes the Trie from `prefixes.json`."""
        print("🔄 Loading IP Prefixes into Trie...")
        load_prefixes(cls._trie)
        print(f"✅ Trie Initialized with {cls._trie.node_count} nodes.")

    @classmethod
    def lookup(cls, ip_address):
        """Performs a lookup for a single IP address."""
        with cls._lock:
            return cls._trie.search(ip_address)

    @classmethod
    def batch_lookup(cls, ip_list):
        """Performs batch lookup for a list of IPs using parallel processing."""
        with cls._lock:
            results = list(cls._executor.map(cls._trie.search, ip_list))
        return results
