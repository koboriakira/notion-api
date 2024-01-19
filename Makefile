dev:
	docker compose up -d
	open http://localhost:10119/docs

cdk-test:
	cd cdk && npm run test
