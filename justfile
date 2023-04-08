run:
    poetry run python src/main.py


check:
    -ruff check . --no-fix
    -mypy .
    -black --check .

check-fix:
    -ruff check . --fix --show-fixes
    -mypy .
    -black .
