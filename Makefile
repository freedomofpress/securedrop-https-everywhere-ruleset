timestamp := $(shell cat latest-rulesets-timestamp)
image := fpf.local/securedrop-https-everywhere-ruleset:$(timestamp)

.PHONY: test-key
test-key: ## Generates a test key for development/testing purposes locally.
	openssl genrsa -out key.pem 4096
	openssl rsa -in key.pem -outform PEM -pubout -out public.pem
	python jwk.py > test-key.jwk

.PHONY: serve
serve: ## Builds Nginx container to serve generated files
	@docker build --build-arg "timestamp=$(timestamp)" -t "$(image)" -f docker/Dockerfile .
	@echo "=============================================================================="
	@echo "          Serving ruleset at http://localhost:4080/https-everywhere/          "
	@echo "=============================================================================="
	@docker run --rm -p 4080 "$(image)"

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
