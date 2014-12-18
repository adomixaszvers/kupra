venv: venv/bin/activate
venv/bin/activate: requirements.txt
	test -d venv || virtualenv venv --python=/usr/bin/python2&& \
	venv/bin/pip install -r requirements.txt&& \
	touch venv/bin/activate;

devbuild: venv
	venv/bin/python wsgi/openshift/manage.py syncdb;

run: devbuild
	venv/bin/python wsgi/openshift/manage.py runserver;
