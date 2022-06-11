TEST_PATH=./

.DEFAULT_GOAL := help

.PHONY: help algolink-websocket venv start-prod dependencies test-dependencies abtesting clean-pyc test start-server test-models-endpoint test-metadata-endpoint test-predict-endpoint

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

algolink-websocket: ## deplpy and train model socket
	gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:5001  model_websocket_service:app

venv: ## create virtual environment
	python3 -m venv venv && source venv/bin/activate

dependencies: ## install dependencies from requirements.txt
	tar xvf modelcloud-0.2.0.tar.gz &&     pip install ./modelcloud-0.2.0/ -i https://pypi.tuna.tsinghua.edu.cn/simple &&  pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple && pip install ./bolt4ds-0.2.0/ -i https://pypi.tuna.tsinghua.edu.cn/simple

test-dependencies: ## install dependencies from test_requirements.txt
	pip install -r test_requirements.txt

abtesting: ## start ab server e.g. make abtesting abport=9001
	gunicorn --access-logfile - -w 8 -b 0.0.0.0:${abport} \
	--worker-class=gevent abtesting.abtools.server:start > \
	run_ab.log 2>&1 &

clean-pyc: ## Remove python artifacts.
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

clean-test:	## Remove test artifacts
	rm -rf .pytest_cache

clean-venv: ## remove all packages from virtual environment
	pip freeze | grep -v "^-e" | xargs pip uninstall -y

test: clean-pyc ## Run unit test suite.
	py.test --verbose --color=yes $(TEST_PATH)

start-server: ## start the local development server
	export APP_SETTINGS="server.config.DevelopmentConfig"; \
	export FLASK_APP=backend/app; \
	export FLASK_DEBUG=1; \
    export FLASK_RUN_HOST="0.0.0.0"; \
    export FLASK_RUN_PORT=5000; \
	flask run
start-prod: ## start the local production server
	gunicorn --workers=3 -b 0.0.0.0:8902  server.wsgi:app >>web-predict.log;

test-models-endpoint: ## test the models endpoint
	curl --request GET --url http://localhost:5000/api/models

test-metadata-endpoint: ## test the metadata endpoint
	curl --request GET --url http://localhost:5000/api/models/iris_model/metadata

test-predict-endpoint: ## test the predict endpoint
	curl --request POST --url http://localhost:5000/api/models/iris_model/predict \
	--header 'content-type: application/json' \
	--data '{"petal_length": 1.0, "petal_width": 1.0, "sepal_length": 1.0, "sepal_width": 1.0}'
test22:
	ls ./