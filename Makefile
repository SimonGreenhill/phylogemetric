.PHONY: build release test clean

build:
	@python -m build

release:
	@twine upload --skip-existing --verbose dist/*

test:
	@tox

quicktest:
	@tox -q -e py39

clean:
	find . -name __pycache__ | xargs rm -rf
	rm -rf build/*

