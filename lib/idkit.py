"""Paper-id helper: dn() is the normalized match key used for every join (lowercase, alphanumeric only)."""
import re
def dn(doi):
    return re.sub(r"[^a-z0-9]", "", (doi or "").lower())
