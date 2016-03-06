install:
	pip install -r requirements.txt

run:
	honcho start local

test:
	nosetests tests/ \
		--verbose \
		--nocapture \
		--with-coverage \
		--cover-package=./src \
		--cover-erase
