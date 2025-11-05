# Contributing to marketspec

## Workflow
1. Fork repo.
2. `git checkout -b feat/name`
3. `pip install -e . pytest ruff mypy`
4. `pytest -q`
5. `ruff check .`
6. `mypy src`
7. Open PR with clear change and examples.

## Standards
- Python 3.9+
- No runtime deps
- Deterministic behavior
- Small surface area
- Strict types and tests
- One-line user API is priority: `venue_symbol(...)`

## Add an exchange
1. New file: `src/marketspec/exchanges/<name>.py`
2. Register resolver:

   ```python
   from ..registry import register
   from ..types import Spec
   from ..unified import _yyyymmdd, _format_strike

   @register("myexchange")
   def _myexchange(s: Spec) -> str:
       return "..."  # return venue symbol
