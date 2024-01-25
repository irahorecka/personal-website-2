black: ## Black format every python file to line length 100
	find . -type f -name "*.py" | xargs black --line-length=120;
	find . -type f -name "*.py" | xargs absolufy-imports;
	make clean;

flake: ## Flake8 every python file
	find . -type f -name "*.py" -a | xargs flake8;

pylint: ## Pylint every python file
	find . -type f -name "*.py" -a | xargs pylint;

clean: ## Remove pycache
	find . -type d -name "__pycache__" | xargs rm -r;
	find . -type f -name ".DS_Store" | xargs rm -r;

minify: ## Minify all .css and .js files
	bash ./scripts/bash/minify-css-js.sh

production: ## Build production web folder
	bash ./prod.sh;
