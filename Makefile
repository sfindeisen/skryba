PYMAIN=src/main/py
PYTEST=src/test/py

.PHONY : default
default: help

.PHONY : help
help:
	@echo 'Available targets:'
	@echo '    test         - run unit tests'
	@echo '    clean        - remove backup files'

.PHONY : test
test: export PYTHONPATH=$(PYMAIN)
test:
	$(PYTEST)/test_collection.py

.PHONY : clean
clean :
	find . -name '*~' -type f -print0 | xargs -0 -p /bin/rm -f
