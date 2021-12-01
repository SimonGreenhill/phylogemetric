.PHONY: build release test clean

build:
	python setup.py sdist bdist_wheel

release:
	python setup.py sdist bdist_wheel upload

test:
	py.test --durations 0 --cov phylogemetric/

clean:
	find . -name __pycache__ | xargs rm -rf
	rm -rf build/*

