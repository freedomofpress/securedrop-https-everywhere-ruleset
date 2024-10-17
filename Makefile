image := fpf.local/securedrop-https-everywhere-ruleset:$(shell cat latest-rulesets-timestamp)

DEFAULT_GOAL: help

.PHONY: check-black
check-black: ## Check Python source code formatting with black
	@poetry run black --check --diff ./

.PHONY: black
black: ## Format Python source code with black
	@poetry run black ./

.PHONY: test-key
test-key: ## Generates a test key for development/testing purposes locally.
	openssl genrsa -out key.pem 4096
	openssl rsa -in key.pem -outform PEM -pubout -out public.pem
	poetry run python jwk.py > test-key.jwk

.PHONY: generate
generate: ## Regenerates rulesets in preparation for signing ceremony
	echo "Generating SecureDrop Onion Name rulesets..."
	poetry run python3 sddir.py
	poetry run python3 upstream/merge-rulesets.py --source_dir rulesets

.PHONY: sign
sign: ## Signs the latest ruleset
	echo "Preparing rulesets for airgapped signature request..."
	./upstream/async-request.sh public_release.pem .
	echo "Updating index for SecureDrop rules..."
	./update_index.sh
	echo "Finished. Please review local changes, and commit as appropriate."

.PHONY: serve
serve: ## Builds Nginx container to serve generated files
	@docker build -t "$(image)" -f docker/Dockerfile .
	@echo "=============================================================================="
	@echo "          Serving ruleset at http://localhost:4080/https-everywhere/          "
	@echo "=============================================================================="
	@docker run --rm -p 127.0.0.1:4080:4080 "$(image)"

.PHONY: verify
verify: ## Verifies the signature of the latest ruleset. Requires openssl to be installed.
	@echo "Attempting to verify ruleset signature using openssl."
	@./scripts/verify
	@poetry run pytest -v

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
