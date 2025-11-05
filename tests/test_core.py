import pytest

from marketspec import Spec, parse_unified_symbol, resolve_venue_symbol
from marketspec.registry import register, resolve  # moved to top


def test_parse_spot():
    d = parse_unified_symbol("BTC/USDT")
    assert d["type"] == "spot" and d["base"] == "BTC" and d["quote"] == "USDT"


def test_resolve_binance_linear_perp():
    d = parse_unified_symbol("BTC/USDT:USDT")
    spec = Spec(**d)
    assert resolve_venue_symbol(exchange="binance", spec=spec) == "BTCUSDT"


def test_resolve_bybit_inverse_future():
    d = parse_unified_symbol("BTC/USD:USD-20251227")
    spec = Spec(**d)
    assert resolve_venue_symbol(exchange="bybit", spec=spec) == "BTCUSD_20251227"


def test_option_strike_formatting():
    # 2500.0 → "2500"; 0.001 → "0.001"
    d = parse_unified_symbol("ETH-20251226-2500-C")
    s = Spec(**d)
    assert resolve_venue_symbol(exchange="binance", spec=s) == "ETH-20251226-2500-C"
    d2 = parse_unified_symbol("ETH-20251226-0.001-P")
    s2 = Spec(**d2)
    assert resolve_venue_symbol(exchange="bybit", spec=s2) == "ETH-20251226-0.001-P"


def test_illegal_symbol_characters_rejected():
    d = parse_unified_symbol("BTC/USDT:USDT")
    s = Spec(**d)
    @register("badx")
    def _bad(_):  # type: ignore
        return "BTC-USDT"  # hyphen not allowed for venue symbols
    with pytest.raises(ValueError, match="Illegal characters"):
        resolve("badx", s)


def test_mismatch_linear_and_settle_blocks():
    # Construct Spec manually to bypass parser consistency checks
    s = Spec(base="BTC", quote="USDT", type="swap", linear=False, settle="USDT", expiry=None)
    err_pat = (
        "linear contract must settle in quote"
        "|inverse contract must settle in USD"
    )
    with pytest.raises(ValueError, match=err_pat):
        resolve_venue_symbol(exchange="binance", spec=s)
