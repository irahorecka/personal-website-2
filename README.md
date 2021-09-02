# pweb2-dev
Second iteration of my personal website.

## Starting up the web app
1. Start up a Python virtual environment and download requirements via `$ pip install -r requirements.txt`
2. Download local npm packages via `$ npm install`. You may need to install PostCSS globally as well: `$ npm install --global postcss postcss-cli`
3. Start the web app via `$ python run.py`

## Shell commands
1. `/scripts/bash/minify_layout.sh` : Minifies CSS and JS hrefs in `/irahorecka/templates/layout.html`.
2. `/scripts/bash/minify-css-js.sh` : Minifies all CSS and JS files recursively.
3. `/prod.sh` : Converts current directory (pweb2-dev) to a production-ready directory (pweb2). Have pweb2 cloned in the directory where pweb2-dev resides. Only changes made to pweb2-dev not yet committed to pweb2 will show. Run this command when you're ready to commit changes made in pweb2-dev to pweb2.
4. `/cron.sh` : Sets cron tasks to execute `/update_db.py` and `rm_expired-db.py`. Remove repetitive cron tasks by first checking `$ crontab -e` then `$ crontab -r` prior to calling `/cron.sh`.

## Things to note
You'll notice there's a `/prod` directory. This directory contains files that are configured for a production environment. If you need to make changes to files found in `/prod` outside of `/prod`, make sure to also sync up the matching file in `/prod`. The `/prod` directory will be removed when migrating pweb2-dev to pweb2 via `/prod.sh`.

## Troubleshooting
When executing `postcss` through the command line you'll sometime receive an error stating a missing `async` javascript library. The best way to alleviate fix this is to delete `/node_modules` and run `npm install`. This should recreate the `/node_modules` directory and `postcss` should work.

## Useful resources:
- [Rapid prototyping with Flask and Tailwind CSS](https://testdriven.io/blog/flask-htmx-tailwind/)
