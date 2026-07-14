"""Authority simulation for the isolation proof.

This is NOT real auth. A token present in principals.json stands in for a verified JWT
signature; presence == valid signature, absence == rejected. The point is the trust
boundary, not the crypto.

Two rules, enforced here and never trusted from the caller:
  - the tenant comes ONLY from the principal, so a seller cannot even name a deal outside
    their own org (cross-tenant ids are unrepresentable).
  - the requested deal must be in the principal's grant list (the per-deal fence).

The seller's question text never passes through here. Identity and scope are settled
before the agent is built, from the token, not from anything the seller types.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

_STORE = Path(__file__).with_name("principals.json")


@dataclass(frozen=True)
class Principal:
    seller_id: str
    name: str
    tenant_id: str
    deals: tuple[str, ...]   # account names this seller may open, within their tenant


class AuthError(Exception):
    """Unknown or blank token. Stands in for a failed signature check."""


class AccessDenied(Exception):
    """A real seller asking for a deal that is not granted to them."""


def _load() -> dict:
    return json.loads(_STORE.read_text())


def authenticate(token: str) -> Principal:
    """Trusted identity from the token. Unknown token is rejected like a bad signature."""
    p = _load().get(token)
    if p is None:
        raise AuthError("invalid or expired token")
    return Principal(
        seller_id=p["seller_id"],
        name=p["name"],
        tenant_id=p["tenant_id"],
        deals=tuple(p["deals"]),
    )


def authorize(principal: Principal, deal: str) -> str:
    """Map a requested deal NAME to its scoped account_id, or refuse.

    `deal` is the only caller-supplied value and can only ever be a name. The tenant is
    taken from the principal, so the returned id is always inside the seller's own org.
    """
    if deal not in principal.deals:
        raise AccessDenied(f"{principal.name} has no access to deal {deal!r}")
    return f"{principal.tenant_id}::{deal}"


def open_deal(token: str, deal: str) -> tuple[Principal, str]:
    """authenticate + authorize. Returns (principal, account_id) or raises."""
    principal = authenticate(token)
    return principal, authorize(principal, deal)
