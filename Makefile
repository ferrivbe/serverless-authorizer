.DEFAULT_GOAL := help

.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: venv
venv:
	@python3 -m pip install virtualenv\
		&& python3 -m virtualenv venv\
		&& . venv/bin/activate\
		&& python3 -m pip install -r functions/user-api/src/requirements.txt\
		&& python3 -m pip install -r functions/user-api/src/requirements.local.txt

.PHONY: venv-local-api
venv-local-api:
	@. venv/bin/activate\
		&& cd functions/user-api/src\
		&& uvicorn handler:app --reload --port 8000

.PHONY: local-api
local-api: venv venv-local-api
