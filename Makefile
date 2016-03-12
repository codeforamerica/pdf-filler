TEST_SCOPE=tests/

install:
	pip install -r requirements.txt

run:
	honcho start local

test:
	nosetests $(TEST_SCOPE) \
		--verbose \
		--nocapture \
		--with-coverage \
		--cover-package=./src \
		--cover-erase

SCOPE=tests/unit
test.unit:
	nosetests $(SCOPE) \
		--verbose \
		--nocapture \
		--with-coverage \
		--cover-package=./src \
		--cover-erase