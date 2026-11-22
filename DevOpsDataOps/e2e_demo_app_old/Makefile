install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vvv --cov=hello --cov=greeting \
		--cov=smath --cov= web tests
	python -m pytest --nbval notebook.ipynb #test our jupyter notebook


debug:
	python -m pytest -vv --pdb #Debbuger is invoked

one-test:
	python -m pytest -vv test/test_greeting.py::test_my_name4

format:
	black *.py

lint:
	pyling --disable=R,C *.py

all: install lint test format