UV=uv

PYTHON=python3

SRC=src

install:
	@$(UV) sync || true

run:
	@$(UV) run $(PYTHON) -m $(SRC) || true

debug:
	@$(PY) -m $(PDB) $(SRC) || true

clean:
	@cleanpy .

lint:
	@flake8 $(SRC) || true
	@mypy $(SRC) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --follow-imports=skip || true