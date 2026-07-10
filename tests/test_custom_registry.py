import investpy


def test_load_registry_includes_custom_currency_rows():
    from investpy.utils.resources import load_registry
    df = load_registry("currency_crosses.csv")
    assert "XPT/USD" in set(df["name"])
    assert "XPD/USD" in set(df["name"])


def test_load_registry_dedupes_on_id_keeping_custom():
    from investpy.utils.resources import load_registry
    df = load_registry("currency_crosses.csv")
    assert df["id"].duplicated().sum() == 0


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
