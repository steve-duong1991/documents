.PHONY: validate validate-external build build-all check help

help:
	@echo "make validate          — check internal markdown links + anchors + README TOC + prose lint"
	@echo "make validate-external — also check https:// links (slow; optional)"
	@echo "make check             — validate, acronym check, build-all, GUIDE.md drift check"
	@echo "make build-all         — rebuild all GUIDE.md from includes/"
	@echo "make build GUIDE=name  — rebuild one guide (e.g. GUIDE=api-design-and-protection)"

validate:
	python3 scripts/validate-doc-links.py
	python3 scripts/validate-doc-readme.py
	python3 scripts/validate-doc-prose.py

validate-external:
	python3 scripts/validate-doc-links.py --external

check: validate
	python3 scripts/expand-acronyms.py --check
	$(MAKE) build-all
	@git diff --quiet -- '*.md' 2>/dev/null || (echo "GUIDE.md out of sync — run make build-all and commit" >&2; git diff --stat -- '*.md'; exit 1)

build-all:
	python3 scripts/build-guide.py

build:
	python3 scripts/build-guide.py $(GUIDE)
