.PHONY: clean data lint requirements docs

# directories that contain python scripts in the codebase
python_files=$$(git ls-files -- . | grep -v "legacy" | grep -v "wip" | grep "\.py$$")

#################################################################################
# Rules
#################################################################################

## ==== codebase ====

## Format codebase, no imports
fmt-base:
	python -m autoflake \
		--in-place --recursive \
		$(python_files)
	python -m isort -rc --honor-noqa \
		$(python_files)
	python -m black \
		$(python_files)

## Format codebase
fmt:
	python -m autoflake \
		--in-place --remove-all-unused-imports --recursive \
		$(python_files)
	python -m isort -rc --honor-noqa \
		$(python_files)
	python -m black \
		$(python_files)

## Lint codebase
lint:
	python -m flake8 \
		$(python_files)
	python -m mypy \
		$(python_files)

## ==== analysis ====

## biorxiv_flow_get_sample
biorxiv_flow_get_sample:
	python scripts/biorxiv_flow_get_sample.py run

## biorxiv_flow_scraping
biorxiv_flow_scraping:
	python scripts/biorxiv_flow_scraping.py run

## medrxiv get abstracts, real thing
medrxiv_flow_get_sample:
	python scripts/medrxiv_flow_get_sample.py run \
		--interval "2020-01-01/2021-12-31"

## medrxiv make triples
medrxiv_flow_make_triples:
	python scripts/medrxiv_flow_make_triples.py run \
		--interval "2020-01-01/2021-12-31"

## medrxiv make ents
medrxiv_flow_make_ents:
	python scripts/medrxiv_flow_make_ents.py run \
		--interval "2020-01-01/2021-12-31" \
		--num_workers 8

## medrxiv make evidence
medrxiv_flow_make_evidence:
	python scripts/medrxiv_flow_make_evidence.py run \
		--interval "2020-01-01/2021-12-31" \
		--num_workers 8

## ==== others ====

## efo
efo:
	python scripts/efo_processing.py run

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}'
