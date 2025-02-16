# 🌍 IP Prefix Lookup API  
A **high-performance** FastAPI service for **IP prefix lookups** using a **Compressed Radix Trie**.  
Supports **IPv4/IPv6 prefix matching** and **batch lookups**.  

---

## 📌 Features  
✅ **Fast IP lookups** using a **Compressed Radix Trie** (O(log N) time complexity)   
✅ **Batch lookup support**   
✅ **Supports IPv4 & IPv6 prefixes** (e.g., `192.168.1.0/24`, `2607:f8b0::/32`)   
✅ **Fully Dockerized**  

---

## 📌 Installation & Setup  
### 🔹 Prerequisites  
- **Python 3.9+**  
- **Docker & Docker Compose** (for containerized setup)

### 🔹 Clone the Repository  
```bash
git clone https://github.com/ambikeshwar1991/ip_prefix_lookup.git
cd ip-prefix-lookup
```

### 🔹 Build and start the container  
```bash
docker-compose up -d --build
```
