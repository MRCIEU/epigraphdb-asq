.PHONY: clean data lint requirements docs

# directories that contain python scripts in the codebase
PYTHON_DIRS = app tests /common_processing/src/common_processing

#################################################################################
# Rules
#################################################################################

## ==== running the api ====

## Start API server, port: 80
run:
	uvicorn app.main:app --reload \
    --reload-dir /app/app \
    --reload-dir /common_processing/src \
	--host 0.0.0.0 --port 80

## Start API server, port: 80, prod, ie no reload
run_prod:
	uvicorn app.main:app \
	--host 0.0.0.0 --port 80

## ==== codebase ====

## Format codebase, no imports
fmt-base:
	for dir in $(PYTHON_DIRS); do \
	  python -m autoflake \
		  --in-place --recursive \
		  $$dir; \
	  python -m isort -rc --honor-noqa \
		  $$dir; \
	  python -m black $$dir; \
	done

## Format codebase
fmt:
	for dir in $(PYTHON_DIRS); do \
	  python -m autoflake \
		  --in-place --remove-all-unused-imports --recursive \
		  $$dir; \
	  python -m isort -rc --honor-noqa \
		  $$dir; \
	  python -m black $$dir; \
	done

## Lint codebase
lint:
	for dir in $(PYTHON_DIRS); do \
	  python -m flake8 \
		  $$dir; \
	  python -m mypy \
		  $$dir; \
	done

## Unit tests
test:
	python -m pytest -vv

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
