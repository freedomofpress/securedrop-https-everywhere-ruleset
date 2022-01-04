image := fpf.local/securedrop-https-everywhere-ruleset:$(shell cat latest-rulesets-timestamp)

DEFAULT_GOAL: rules

.PHONY: check-black
check-black: ## Check Python source code formatting with black
	@black --check --diff ./

.PHONY: black
black: ## Format Python source code with black
	@black ./

.PHONY: test-key
test-key: ## Generates a test key for development/testing purposes locally.
	openssl genrsa -out key.pem 4096
	openssl rsa -in key.pem -outform PEM -pubout -out public.pem
	python jwk.py > test-key.jwk

.PHONY: rules
rules: ## Regenerates rulesets in preparation for signing ceremony
	./scripts/generate-and-sign

.PHONY: serve
serve: ## Builds Nginx container to serve generated files
	@docker build -t "$(image)" -f docker/Dockerfile .
	@echo "=============================================================================="
	@echo "          Serving ruleset at http://localhost:4080/https-everywhere/          "
	@echo "=============================================================================="
	@docker run --rm -p 127.0.0.1:4080:4080 "$(image)"

.PHONY: venv
venv: ## Provision a Python 3 virtualenv for development
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip wheel
	.venv/bin/pip install --require-hashes -r "dev-requirements.txt"
	.venv/bin/pip install --require-hashes -r "requirements.txt"
	@echo "#################"
	@echo "Make sure to run: source .venv/bin/activate"

.PHONY: verify
verify: ## Verifies the signature of the latest ruleset. Requires openssl to be installed.
	@echo "Attempting to verify ruleset signature using openssl."
	@./scripts/verify

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
