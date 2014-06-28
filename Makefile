test: .env/requirements.lock
	.env/bin/tox

.env/requirements.lock: .env
	.env/bin/pip install tox
	.env/bin/pip freeze > .env/requirements.lock

.env:
	pip install virtualenv
	virtualenv .env
