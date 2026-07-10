import investpy
import pytest

_RECENT = ("01/06/2026", "10/07/2026")


@pytest.mark.network
@pytest.mark.parametrize("fn,args", [
    (investpy.get_currency_cross_historical_data, ("XPT/USD", *_RECENT)),
    (investpy.get_currency_cross_historical_data, ("XPD/USD", *_RECENT)),
    (investpy.get_index_historical_data, ("Baltic Dry Index", "united kingdom", *_RECENT)),
    (investpy.get_index_historical_data, ("SSE Star 50", "china", *_RECENT)),
    (investpy.get_index_historical_data, ("MSCI Intl Emerging Market Currency", "world", *_RECENT)),
    (investpy.get_stock_historical_data, ("688256", "china", *_RECENT)),
    (investpy.get_stock_historical_data, ("688165", "china", *_RECENT)),
    (investpy.get_stock_historical_data, ("603501", "china", *_RECENT)),
])
def test_direct_path_resolves_each_pin(fn, args):
    df = fn(*args)
    assert not df.empty and "Close" in df.columns


def test_load_registry_includes_custom_currency_rows():
    from investpy.utils.resources import load_registry
    df = load_registry("currency_crosses.csv")
    assert "XPT/USD" in set(df["name"])
    assert "XPD/USD" in set(df["name"])


def test_load_registry_dedupes_on_id_keeping_custom():
    from investpy.utils.resources import load_registry
    df = load_registry("currency_crosses.csv")
    assert df["id"].duplicated().sum() == 0


def test_stock_list_symbols_are_strings():
    symbols = investpy.get_stocks_list()
    assert all(isinstance(symbol, str) for symbol in symbols)
    assert "688256" in investpy.get_stocks_list(country="china")


def test_index_countries_include_overlay():
    from investpy.utils.resources import load_registry
    indices = load_registry("indices.csv")
    assert set(indices["country"]) <= set(investpy.get_index_countries())


def test_list_functions_include_custom_rows():
    assert "XPT/USD" in investpy.get_currency_crosses_list()
    assert "XPD/USD" in investpy.get_currency_crosses_list()
    assert "Baltic Dry Index" in investpy.get_indices_list()
    assert "SSE Star 50" in investpy.get_indices_list(country="china")
    assert "MSCI Intl Emerging Market Currency" in investpy.get_indices_list(country="world")
    assert "world" in investpy.get_index_countries()
    assert "688256" in investpy.get_stocks_list(country="china")
    assert "688165" in investpy.get_stocks_list(country="china")
    assert "603501" in investpy.get_stocks_list(country="china")
