#!/usr/bin/env bash

# Convert ./irahorecka/templates/layout.html to a minified version
# Store output as ./prod/irahorecka/templates/layout.html
mkdir ./prod/irahorecka/templates;
cp ./irahorecka/templates/layout.html ./prod/irahorecka/templates/layout.html;
perl -i -p0e 's/{% assets.*?assets %}/<link rel="stylesheet" href="{{ url_for('\''static'\'', filename='\''css\/dist\/main.min.css'\'') }}">/s' ./prod/irahorecka/templates/layout.html;
sed -i '' '/.min.js/! s/\([^.]*\)\.js/\1.min.js/g' ./prod/irahorecka/templates/layout.html;
sed -i '' '/.min.cs/! s/\([^.]*\)\.css/\1.min.css/g' ./prod/irahorecka/templates/layout.html;
