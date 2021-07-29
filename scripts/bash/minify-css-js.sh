#!/usr/bin/env bash

# Noob bash script to convert any *.js file to *.min.js
for i in $(find ./irahorecka -type f -name "*.js")
do
    if [[ $i == *".min.js" ]]
    then
        echo will not modify $i
    else
        i2=${i%".js"}
        echo modify $i2 to "${i2}.min.js"
        uglifyjs $i -o "${i2}.min.js";
    fi
done

# Convert any *.css file to *.min.css
for i in $(find ./irahorecka -type f -name "*.css")
do
    if [[ $i == *".min.css" ]]
    then
        echo will not modify $i
    else
        i2=${i%".css"}
        echo modify $i2 to "${i2}.min.css"
        uglifycss $i --output "${i2}.min.css"
    fi
done
