dev:
	docker compose up --build -d
	open http://localhost:10119/docs

cdk-test:
	cd cdk && npm run test

.PHONY: test
test:
	@pipenv run pytest -m "not slow and not learning and not use_genuine_api"

.PHONY: test-current
test-current:
	@pipenv run pytest -m "current"


.PHONY: gauge
gauge:
	cd e2e && gauge run specs

.PHONY: gauge-current
gauge-current:
	cd e2e && gauge run --tags "current" specs
