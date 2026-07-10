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
