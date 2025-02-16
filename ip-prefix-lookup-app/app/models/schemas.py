from pydantic import BaseModel, IPvAnyAddress, IPvAnyNetwork, Field
from typing import List


class IPRequest(BaseModel):
    """
    Schema for single IP lookup request.

    - `ip`: valid IPv4/IPv6 addresse.
    - Ensures one IP is provided.
    """
    ip: IPvAnyAddress


class BatchIPRequest(BaseModel):
    """
    Schema for batch IP lookup request.

    - `ips`: List of valid IPv4/IPv6 addresses.
    - Ensures at least one IP is provided.
    """

    ips: List[IPvAnyAddress] = Field(
        ...,
        min_length=1,
        title="IP List",
        description="List of valid IPv4/IPv6 addresses.",
    )
