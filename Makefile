
.PHONY: lint
lint: export PYTHONPATH:= resources:tests
lint:
	# exclude resource01 -- has deliberate bugs for pyflakes
	pyflakes resources/resource0[2-6]*py tests/talktests/*py
	# exclude resource01, resource02 -- have deliberate bugs for pylint
	pylint --rcfile=pylintrc resources/resource0[3-6]*py tests/talktests/*py


.PHONY: tests
tests: export PYTHONPATH:= resources:tests
tests:
	trial talktests

test: tests

