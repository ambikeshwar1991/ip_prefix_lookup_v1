import time
import psutil
import json
import ipaddress
from app.models.trie import IPTrie
from app.services.data_loader import load_prefixes

# Load prefixes.json
with open("data/prefixes.json", "r") as f:
    data = json.load(f)

# Extract test prefixes for IPv4 & IPv6
ipv4_prefixes = []
ipv6_prefixes = []
for provider, entries in data.items():
    for entry in entries:
        for prefix in entry["prefixes"]:
            if ":" in prefix:
                ipv6_prefixes.append(prefix)  # IPv6
            else:
                ipv4_prefixes.append(prefix)  # IPv4

# Generate sample IPs from prefixes
def generate_sample_ips(prefix_list, count=100):
    """Generate sample IPs from given prefixes"""
    sample_ips = []
    for prefix in prefix_list[:count]:  # Take `count` prefixes
        network = ipaddress.ip_network(prefix, strict=False)
        sample_ips.append(
            str(network.network_address + 50)
        )  # Pick a random IP in range
    return sample_ips


sample_ipv4_ips = generate_sample_ips(ipv4_prefixes, 100)
sample_ipv6_ips = generate_sample_ips(ipv6_prefixes, 100)

# Generate Not Found IPs (IPs outside known ranges)
not_found_ips = [
    "203.0.113.255",  # Reserved IP (not in dataset)
    "192.0.2.123",  # Another reserved IP
    "fd00::abcd",  # IPv6 Unique Local Address (ULA)
    "2607:f8b0::9999",  # Random IPv6 outside dataset
]

# Generate IPs that match multiple subnets
multi_match_ips = [
    "23.79.237.45",  # Example IP known to match multiple subnets
    "184.51.33.230",  # Another example of a multi-subnet match
]

# Initialize Trie
trie = IPTrie()

### **Benchmark 1: Measure Memory Usage Before and After Trie Load**
process = psutil.Process()
memory_before = process.memory_info().rss  # Resident Set Size (RAM usage)

start_time = time.time()
load_prefixes(trie)  # Load data into Trie
end_time = time.time()

memory_after = process.memory_info().rss
memory_used = (memory_after - memory_before) / (1024 * 1024)  # Convert bytes to MB

print(f"Trie Loaded in {end_time - start_time:.4f} seconds")
print(f"Memory Used: {memory_used:.2f} MB")
print(f"Total Trie Nodes: {trie.node_count}")

### **Benchmark 2: Single IP Lookup Speed (Found, Not Found, Multi-Match)**
def benchmark_lookup(trie, ips, label="Lookup"):
    """Benchmark lookup performance"""
    lookup_times = []
    for ip in ips[:10]:  # Test first 10 IPs
        start = time.time()
        _ = trie.search(ip)
        end = time.time()
        lookup_times.append((end - start) * 1000)  # Convert to ms
    avg_time = sum(lookup_times) / len(lookup_times)
    print(f"{label} Avg Time: {avg_time:.4f} ms")
    return avg_time


benchmark_lookup(trie, sample_ipv4_ips, "IPv4 Lookup (Found)")
benchmark_lookup(trie, sample_ipv6_ips, "IPv6 Lookup (Found)")
benchmark_lookup(trie, not_found_ips, "IP Lookup (Not Found)")
benchmark_lookup(trie, multi_match_ips, "IP Lookup (Multi-Match)")

### **📌 Benchmark 3: Batch Lookup Speed (10 IPs at a time, Found, Not Found, Multi-Match)**
def benchmark_batch_lookup(trie, ips, label="Batch Lookup"):
    """Benchmark batch lookup performance"""
    batch_lookup_times = []
    for i in range(0, len(ips), 10):
        batch = ips[i : i + 10]  # Take 10 IPs at a time
        start = time.time()
        for ip in batch:
            trie.search(ip)
        end = time.time()
        batch_lookup_times.append((end - start) * 1000)  # Convert to ms
    avg_time = sum(batch_lookup_times) / len(batch_lookup_times)
    print(f"{label} (10 IPs) Avg Time: {avg_time:.4f} ms")
    return avg_time


benchmark_batch_lookup(trie, sample_ipv4_ips, "IPv4 Batch Lookup (Found)")
benchmark_batch_lookup(trie, sample_ipv6_ips, "IPv6 Batch Lookup (Found)")
benchmark_batch_lookup(trie, not_found_ips * 10, "Batch Lookup (Not Found)")
benchmark_batch_lookup(trie, multi_match_ips * 10, "Batch Lookup (Multi-Match)")
