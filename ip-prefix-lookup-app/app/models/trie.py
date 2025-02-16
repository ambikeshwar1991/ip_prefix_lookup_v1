import ipaddress
from app.utils.logging_config import logger


class TrieNode:
    """Compressed Radix Trie Node"""

    __slots__ = ("prefix", "children", "data")

    def __init__(self, prefix=""):
        self.prefix = prefix  # Compressed prefix
        self.children = {}
        self.data = []  # Stores multiple subnet matches


class IPTrie:
    """Compressed Radix Trie for IP Prefix Matching."""

    __slots__ = ("root", "node_count")

    def __init__(self):
        self.root = TrieNode()
        self.node_count = 1  # Start with root node
        logger.info("Trie initialized.")

    def insert(self, subnet: str, provider: str, tags: list):
        """Insert an IP subnet into the compressed radix trie and track node count."""
        network = ipaddress.ip_network(subnet, strict=False)
        binary_prefix = self._get_network_bits(network)
        node = self.root

        while binary_prefix:
            for existing_prefix, child in node.children.items():
                common_prefix = self._find_common_prefix(binary_prefix, existing_prefix)

                if common_prefix:
                    if common_prefix == existing_prefix:
                        node = child
                        binary_prefix = binary_prefix[len(common_prefix) :]
                        break
                    else:
                        # Partial match, split the node
                        new_child = TrieNode(common_prefix)
                        new_child.children[
                            existing_prefix[len(common_prefix) :]
                        ] = child
                        node.children[common_prefix] = new_child
                        del node.children[existing_prefix]
                        node = new_child
                        binary_prefix = binary_prefix[len(common_prefix) :]
                        self.node_count += 1
                        break
            else:
                # No match, insert new compressed path
                node.children[binary_prefix] = TrieNode(binary_prefix)
                node = node.children[binary_prefix]
                self.node_count += 1
                break

        # Store data as a dictionary instead of tuple
        node.data.append(
            {
                "subnet": subnet,
                "provider": provider,
                "tags": list(tags),  # Convert tuple to list
            }
        )
        logger.info(
            f"Inserted {subnet} (Provider: {provider}, Tags: {tags}). Total Nodes: {self.node_count}"
        )

    def search(self, ip: str):
        """Find all matching subnets for an IP address and return as a dictionary list."""
        ip_addr = ipaddress.ip_address(ip)
        binary_ip = self._get_ip_bits(ip_addr)
        node = self.root
        matches = []

        while binary_ip:
            for prefix, child in node.children.items():
                if binary_ip.startswith(prefix):
                    node = child
                    binary_ip = binary_ip[len(prefix) :]
                    if node.data:
                        matches.extend(node.data)  # Collect matching subnets
                    break
            else:
                break  # No more matches

        logger.info(f"Search for {ip}: {len(matches)} matches found.")
        return matches if matches else None

    def _get_network_bits(self, network):
        """Convert a network into a binary bit sequence (IP + Prefix length)."""
        return f"{int(network.network_address):032b}"[: network.prefixlen]

    def _get_ip_bits(self, ip_addr):
        """Convert an IP address into a binary bit sequence."""
        return f"{int(ip_addr):032b}"

    def _find_common_prefix(self, a, b):
        """Find the common prefix between two binary strings."""
        length = min(len(a), len(b))
        for i in range(length):
            if a[i] != b[i]:
                return a[:i]
        return a[:length]
