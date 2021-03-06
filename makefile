IDB2.log:
	git log > IDB2.log

IDB3.log:
	git log > IDB3.log

log:
	git log > IDB2.log

models.html: app/models.py
	cd app; pydoc3 -w models; mv models.html ../models.html

test:
	coverage run app/tests.py
	coverage report --include=app/test_models.py,app/tests.py
