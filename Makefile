
.PHONY: tests
tests: export PYTHONPATH:= resources:tests
tests:
	trial talktests

test: tests

