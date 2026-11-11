SHELL := /bin/bash
.PHONY: tools test scan verify
tools:
	bash scripts/install-tools.sh
test:
	python3 -m unittest discover -s tests -v
scan:
	bash scripts/scan.sh all
verify:
	python3 scripts/verify_detection.py
