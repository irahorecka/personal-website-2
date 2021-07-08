black: ## Black format every python file to line length 100
	find . -type f -name "*.py" | xargs black --line-length=120;
	find . -type f -name "*.py" | xargs absolufy-imports;
	make clean;

flake: ## Flake8 every python file
	find . -type f -name "*.py" -a | xargs flake8;

pylint: ## Pylint every python file
	find . -type f -name "*.py" -a | xargs pylint;

postcss: ## Apply postcss to irahorecka/static/src/main.css to irahorecka/static/dist/main.css
	postcss irahorecka/static/src/main.css -o irahorecka/static/dist/main.css

pre-commit: ## Install and autoupdate pre-commit
	pre-commit install;
	pre-commit autoupdate;

clean: ## Remove pycache
	find . -type d -name "__pycache__" | xargs rm -r;
