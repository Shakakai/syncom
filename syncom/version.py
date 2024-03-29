"""The `version` module holds the version information for SynCom."""
from __future__ import annotations as _annotations

__all__ = 'VERSION', 'version_short'

VERSION = '0.1.0'
"""The version of SynCom."""


def version_short() -> str:
    """Return the `major.minor` part of SynCom version.

    It returns '2.1' if SynCom version is '2.1.1'.
    """
    return '.'.join(VERSION.split('.')[:2])
