.PHONY: validate validate-external check github-format help

help:
	@echo "make validate          — check internal markdown links + anchors + README TOC + prose lint"
	@echo "make validate-external — also check https:// links (slow; optional)"
	@echo "make check             — validate + acronym check"
	@echo "make github-format     — clean headings, README TOC links, GLOSSARY links for GitHub"

validate:
	python3 scripts/validate-doc-links.py
	python3 scripts/validate-doc-readme.py
	python3 scripts/validate-doc-prose.py

validate-external:
	python3 scripts/validate-doc-links.py --external

check: validate
	python3 scripts/expand-acronyms.py --check

github-format:
	python3 scripts/github-format.py
