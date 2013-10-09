test: .env/requirements.lock
	.env/bin/nosetests --with-coverage --cover-package=dj_queryset_manager

.env/requirements.lock: .env
	.env/bin/pip install nose coverage Django
	.env/bin/pip freeze > .env/requirements.lock

.env:
	pip install virtualenv
	virtualenv .env
