black:
	black .

pylint:
	pylint app/

isort:
	isort app/

mypy:
	mypy app/

coverage:
	coverage run --source=app -m unittest discover -s tests && coverage report --fail-under=30 --show-missing


make validate:
	make black
	make isort
# 	make mypy
	make pylint
