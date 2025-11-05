import pytest

from marketspec import Spec, parse, resolve_symbol
from marketspec.registry import register, resolve  # keep for registry-level checks


def test_parse_spot():
    s = parse("BTC/USDT")
    assert s.type == "spot" and s.base == "BTC" and s.quote == "USDT"


def test_resolve_binance_linear_perp():
    spec = parse("BTC/USDT:USDT")
    assert resolve_symbol("binance", spec) == "BTCUSDT"


def test_resolve_bybit_inverse_future():
    spec = parse("BTC/USD:USD-20251227")
    assert resolve_symbol("bybit", spec) == "BTCUSD_20251227"


def test_option_strike_formatting():
    # 2500.0 → "2500"; 0.001 → "0.001"
    s = parse("ETH-20251226-2500-C")
    assert resolve_symbol("binance", s) == "ETH-20251226-2500-C"
    s2 = parse("ETH-20251226-0.001-P")
    assert resolve_symbol("bybit", s2) == "ETH-20251226-0.001-P"


def test_illegal_symbol_characters_rejected():
    spec = parse("BTC/USDT:USDT")

    @register("badx")
    def _bad(_):  # type: ignore
        return "BTC-USDT"  # hyphen not allowed for venue symbols

    with pytest.raises(ValueError, match="Illegal characters"):
        resolve("badx", spec)


def test_mismatch_linear_and_settle_blocks():
    # Construct Spec manually to bypass parser consistency checks
    s = Spec(base="BTC", quote="USDT", type="swap", linear=False, settle="USDT", expiry=None)
    err_pat = (
        "linear contract must settle in quote"
        "|inverse contract must settle in USD"
    )
    with pytest.raises(ValueError, match=err_pat):
        resolve_symbol("binance", s)
