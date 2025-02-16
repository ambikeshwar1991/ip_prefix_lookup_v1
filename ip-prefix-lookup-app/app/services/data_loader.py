import json
import os
import time
from app.models.trie import IPTrie
from app.utils.logging_config import logger

DATA_FILE = os.path.join(os.path.dirname(__file__), "../../data/prefixes.json")

def load_prefixes(trie: IPTrie, filename=DATA_FILE):
    """Load prefixes into Trie and log load time & node count."""
    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logger.error(
            f"Failed to load {filename}. Ensure it exists and is valid JSON."
        )
        return

    prefix_count = 0
    start_time = time.time()

    for provider, entries in data.items():
        for entry in entries:
            for subnet in entry.get("prefixes", []):
                trie.insert(subnet, provider, entry.get("tags", []))
                prefix_count += 1

    elapsed_time = time.time() - start_time

    logger.info(
        f"Loaded {prefix_count} subnets into Trie from {filename} in {elapsed_time:.2f} seconds."
    )
    logger.info(f"Total Trie Nodes: {trie.node_count}")
