#!/usr/bin/env bash
# ~~~~~ Execute bash script from project root directory ~~~~~

# ----- Make copy of root directory -----
cd ../;
cp -rf ./personal-website-2 ./personal-website-2-production;
cd personal-website-2-production;

# ----- Remove files and folders -----
# Remove config and npm files/folders from root directory
rm package-lock.json package.json postcss.config.js tailwind.config.js .pre-commit-config.yaml .gitignore LICENSE Makefile README.md prod.sh *.ipynb *.db;
rm -rf .git node_modules;
# Remove extraneous files in project directory
cd ./irahorecka;
rm ./templates/_tailwind_purge.html;
find . -type d -name "__pycache__" | xargs rm -r;
find . -type d -name ".ipynb_checkpoints" | xargs rm -r;
find . -type d -name "archive" | xargs rm -rf;
find . -type d -name "src" | xargs rm -rf;
find . -type d -name ".webassets-cache" | xargs rm -rf;
cd ../;

# ----- Move production files and replace -----
mv ./prod/config.yaml ./config.yaml;
mv ./prod/wsgi.py ./wsgi.py;
mv ./prod/run.py ./run.py;
mv ./prod/irahorecka/__init__.py ./irahorecka/__init__.py;
mv ./prod/irahorecka/templates/layout.html ./irahorecka/templates/layout.html;
mv ./prod/irahorecka/config.py ./irahorecka/config.py;
rm -rf ./prod;

# ----- Fianlly, rename and zip production folder and remove production dir -----
cd ../;
mv ./personal-website-2-production ./personal-website
zip -r9 personal-website.zip ./personal-website;
rm -rf ./personal-website;
