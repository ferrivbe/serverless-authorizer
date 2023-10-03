.DEFAULT_GOAL := help

include .env

.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: install
install:
	@python3 -m pip install virtualenv\
		&& python3 -m virtualenv venv\
		&& . venv/bin/activate\
		&& python3 -m pip install -r functions/api/src/requirements.txt\
		&& python3 -m pip install -r functions/api/src/requirements.local.txt

.PHONY: api
api:
	@. venv/bin/activate\
		&& export CLIENT_ID="${CLIENT_ID}"\
		&& export CLIENT_SECRET="${CLIENT_SECRET}"\
		&& export REGION="${REGION}"\
		&& export SERVICE_ENVIRONMENT="${SERVICE_ENVIRONMENT}"\
		&& export USERPOOL_ID="${USERPOOL_ID}"\
		&& cd functions/api/src\
		&& python3 -m uvicorn handler:app --reload --port 8000

.PHONY: local
local: install api
