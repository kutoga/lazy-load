.PHONY: venv test dist upload_test upload rstcheck

venv:
	@echo "source .venv/bin/activate"

test:
	rm tests/**/*.pyc
	python3 -mpytest ./tests

dist:
	$(RM) -Rf dist
	python3 setup.py sdist bdist_wheel

upload_test: dist
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload: dist
	twine upload dist/*

rstcheck:
	python3 -mrstcheck README.rst

