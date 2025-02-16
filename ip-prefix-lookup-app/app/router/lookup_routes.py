from fastapi import APIRouter, Request, HTTPException
from pydantic import IPvAnyAddress
from app.services.trie_manager import TrieManager
from app.models.schemas import BatchIPRequest
from app.utils.logging_config import logger

router = APIRouter(prefix="/api/v1/lookup", tags=["IP Lookup"])


@router.get("/{ip}")
def get_lookup(ip: IPvAnyAddress):
    """
    🔍 Lookup a single IP using Trie from FastAPI state.

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
    """
    logger.info(f"Single IP lookup request for {ip}")

    result = TrieManager.lookup(str(ip))

    if result is None:
        logger.warning(f"IP {ip} not found in any subnet.")
        raise HTTPException(status_code=404, detail="IP not found in any subnet")

    return {"result": result}


@router.post("/batch")
def post_lookup(request: BatchIPRequest):
    """
    Perform a batch lookup for multiple IPs using Trie from FastAPI state.

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
    """
    logger.info(f"Batch lookup request for {len(request.ips)} IPs.")
    results = TrieManager.batch_lookup([str(ip) for ip in request.ips])

    if all(x is None for x in results):
        raise HTTPException(status_code=404, detail="No IPs found in any subnet")

    return {"result": results}
