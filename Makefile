format:
	poetry run black .
	poetry run isort .

run:
	poetry run python main.py
