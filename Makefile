mypy:
	mypy *.py src/ tests/ --check-untyped-defs

pytest:
	pytest --tb=short


test: mypy pytest
