dev:
	docker compose up -d
	open http://localhost:10119/docs

cdk-test:
	cd cdk && npm run test

.PHONY: test
test:
	@pytest -m "not slow and not learning and not use_genuine_api"
