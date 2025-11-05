# Changelog

## 0.3.0
- Deprecate parse_unified_symbol() in favor of parse() which returns Spec. Still exported and works, but emits DeprecationWarning.
- Deprecate resolve_venue_symbol() in favor of resolve_symbol() (alias of registry.resolve). Still exported and works, but emits DeprecationWarning.
- Add override_stables(stables: set[str]) context manager for safe, scoped override of the stable-coin set.
- Keep global set_stables(...) for coarse control.
- Add Spec.unified() for round-tripping.
- Add ResolveError (subclasses ValueError) for resolution failures. registry.resolve now raises ResolveError instead of plain ValueError.
- Internal: tightened docs and examples. No runtime deps added.

## 0.2.0
- Add stable `parse(unified) -> Spec`.
- Export `resolve_symbol` alias for `registry.resolve`.
- Docs: update README with stable API.

## 0.1.0
- Initial release. Unified parser and resolvers for Binance and Bybit.
