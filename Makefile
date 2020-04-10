.PHONY: test-key
test-key: ## Generates a test key for development/testing purposes locally.
	openssl genrsa -out key.pem 4096
	openssl rsa -in key.pem -outform PEM -pubout -out public.pem
	python jwk.py > test-key.jwk

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
