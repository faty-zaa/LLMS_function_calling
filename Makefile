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
	@flake8 . || true
	@mypy src \
	 --warn-return-any \
    --warn-unused-ignores \
    --disallow-untyped-defs \
    --check-untyped-defs || true