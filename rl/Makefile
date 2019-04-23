# https://github.com/pypa/pipenv/issues/1921
create-pipfile-with-overrides:
	pipenv lock --dev
	pipenv install --dev

kill-virtualenv:
	pipenv --rm

install:
	pipenv shell && \
	pip install gym_unity && \
	pip install tf-agents-nightly && \
	pip install tensorflow==2.0.0-alpha0

run:
	pipenv run python -u main.py