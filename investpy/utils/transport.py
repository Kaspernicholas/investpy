"""Pluggable HTTP transport for every Investing.com request in investpy.

The default sends each request through curl_cffi with Chrome impersonation,
exactly as the inline calls did before. A caller can install any object that
exposes ``post(url, headers, data=None, params=None)`` and
``get(url, headers, params=None)`` and returns something with
``status_code``, ``text`` and ``json()`` — for example a transport that runs
the request inside a real browser so Cloudflare challenges are solved there.

Module state: ``set_transport`` must always be paired with ``reset_transport``
in a ``finally`` block by the caller.
"""

from curl_cffi import requests as _curl

IMPERSONATE = "chrome136"


class CurlTransport(object):
    """Default transport: curl_cffi with the pinned Chrome TLS fingerprint."""

    def post(self, url, headers, data=None, params=None):
        return _curl.post(url, headers=headers, data=data, params=params, impersonate=IMPERSONATE)

    def get(self, url, headers, params=None):
        return _curl.get(url, headers=headers, params=params, impersonate=IMPERSONATE)


_DEFAULT = CurlTransport()
_active = _DEFAULT


def set_transport(transport):
    """Route all subsequent investpy requests through ``transport``."""
    global _active
    _active = transport


def reset_transport():
    """Restore the default curl_cffi transport."""
    global _active
    _active = _DEFAULT


def get_transport():
    return _active


def post(url, headers, data=None, params=None):
    return _active.post(url, headers, data=data, params=params)


def get(url, headers, params=None):
    return _active.get(url, headers, params=params)
