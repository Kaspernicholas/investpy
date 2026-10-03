"""The pluggable transport: default is curl_cffi, any object with get/post can replace it."""

from investpy.utils import transport


class _Recorder:
    def __init__(self):
        self.calls = []

    def post(self, url, headers, data=None, params=None):
        self.calls.append(("POST", url, headers, data, params))
        return "post-result"

    def get(self, url, headers, params=None):
        self.calls.append(("GET", url, headers, params))
        return "get-result"


def test_default_transport_is_curl():
    transport.reset_transport()
    assert isinstance(transport.get_transport(), transport.CurlTransport)


def test_set_transport_routes_post_and_get():
    rec = _Recorder()
    transport.set_transport(rec)
    try:
        assert transport.post("http://x", {"A": "1"}, data={"k": "v"}) == "post-result"
        assert transport.get("http://y", {"B": "2"}, params={"q": "1"}) == "get-result"
        assert transport.post("http://z", {}, params={"p": "1"}) == "post-result"
    finally:
        transport.reset_transport()
    assert rec.calls == [
        ("POST", "http://x", {"A": "1"}, {"k": "v"}, None),
        ("GET", "http://y", {"B": "2"}, {"q": "1"}),
        ("POST", "http://z", {}, None, {"p": "1"}),
    ]


def test_reset_restores_default():
    transport.set_transport(_Recorder())
    transport.reset_transport()
    assert isinstance(transport.get_transport(), transport.CurlTransport)


def test_curl_transport_passes_impersonate(monkeypatch):
    seen = {}

    def fake_post(url, **kw):
        seen["post"] = (url, kw)
        return "r"

    def fake_get(url, **kw):
        seen["get"] = (url, kw)
        return "r"

    monkeypatch.setattr(transport._curl, "post", fake_post)
    monkeypatch.setattr(transport._curl, "get", fake_get)
    t = transport.CurlTransport()
    t.post("http://a", {"H": "1"}, data={"d": 1}, params={"p": 2})
    t.get("http://b", {"H": "2"}, params={"q": 3})
    assert seen["post"] == (
        "http://a",
        {"headers": {"H": "1"}, "data": {"d": 1}, "params": {"p": 2}, "impersonate": "chrome136"},
    )
    assert seen["get"] == (
        "http://b", {"headers": {"H": "2"}, "params": {"q": 3}, "impersonate": "chrome136"}
    )


def test_historical_data_goes_through_transport():
    """A recorded transport sees the HistoricalDataAjax POST; investpy must not
    reach curl_cffi directly."""
    import investpy

    class _Canned(_Recorder):
        status_code = 200

        def post(self, url, headers, data=None, params=None):
            super().post(url, headers, data, params)
            raise RuntimeError("stop-here")

    canned = _Canned()
    transport.set_transport(canned)
    try:
        try:
            investpy.get_currency_cross_historical_data("EUR/USD", "01/06/2026", "10/06/2026")
        except RuntimeError as e:
            assert str(e) == "stop-here"
    finally:
        transport.reset_transport()
    assert canned.calls and canned.calls[0][1].endswith("/instruments/HistoricalDataAjax")
