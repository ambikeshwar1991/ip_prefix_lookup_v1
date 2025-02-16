## IP Prefix Lookup API

**Version**: 1.0.0

**Description**: API for performing IP lookups against cloud provider prefixes and managing prefix updates.

### Paths

#### `/api/v1/lookup/{ip}`

**Method**: `get`

**Summary**: Get Lookup

**Description**: 🔍 Lookup a single IP using Trie from FastAPI state.

- **Validates IP** format before lookup.
- **Returns** matching subnets, provider details, and tags.

Example Request:
```
GET /api/v1/lookup/192.168.1.5
```

Example Response:
```json
{
    "result": [
        {
            "subnet": "192.168.1.0/24",
            "provider": "AWS",
            "tags": ["Cloud"]
        }
    ]
}
```

**Parameters:**
- `ip` (path): No description


#### `/api/v1/lookup/batch`

**Method**: `post`

**Summary**: Post Lookup

**Description**: Perform a batch lookup for multiple IPs using Trie from FastAPI state.

- **Validates IPs** before lookup.
- **Returns a dictionary of matching results**.

Example Request:
```json
{
    "ips": ["192.168.1.1", "2001:db8::ff00:42"]
}
```

Example Response:
```json
{
    "result": {
        "192.168.1.1": [
            { "subnet": "192.168.1.0/24", "provider": "AWS", "tags": ["Cloud"] }
        ],
        "2001:db8::ff00:42": [
            { "subnet": "2001:db8::/32", "provider": "IPv6Provider", "tags": ["IPv6"] }
        ]
    }
}
```

**Parameters:**
None


#### `/api/v1/reload/`

**Method**: `post`

**Summary**: Reload Prefixes

**Description**: Endpoint to manually reload the Trie from `prefixes.json`.

This function:
- Reads the latest `prefixes.json` file.
- Updates the Compressed Radix Trie with new prefix data.
- Logs every reload request for tracking.

Returns:
    JSON response confirming successful reload or an error message.

**Parameters:**
None


#### `/api/v1/`

**Method**: `get`

**Summary**: API Health Check

**Description**: Health check endpoint to verify that the API is running.

- **Returns**: A simple message confirming the service is operational.
- **Example Response**:
```json
{
    "message": "IP Prefix Lookup API is running."
}
```

**Parameters:**
None


