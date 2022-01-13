#!/bin/bash
# Author: Walter Schreppers
# Description: 
# compile production vue widgets and then inject into redactietool flask application 
# some parts blatently copied from here :
#   https://github.com/w-A-L-L-e/bash_renamer
# the audacity of it all ;)

function compile_vue_components() {
  npm run build

  # move newly compiled widgets into flask app (and remove old ones)
  rm -rf ../../app/static/vue/*
  cp -r dist/css ../../app/static/vue
  cp -r dist/js ../../app/static/vue
}

function inject_git_version() {
  echo "<!-- injected from git branch SHA ${2} -->" >> $1
}

function inject_js() {
  ls -1 -r "$1" | grep -v "map" | while read file;
  do
    flask_path=vue/js/${file}
    echo "<link href=\"{{ url_for('static', filename='${flask_path}') }}\" rel=\"preload\" as=\"script\">" >> ../../app/templates/includes/base_vue_header.html
    echo "<script type=\"text/javascript\" src=\"{{ url_for('static', filename='${flask_path}') }}\"></script>" >> ../../app/templates/includes/base_vue_body.html
  done
}

function inject_css() {
  # inject some vue magic includes
  ls -1 -r "$1" | grep "css" | while read file;
  do
    flask_path=vue/css/${file}

    echo "<link href=\"{{ url_for('static', filename='${flask_path}') }}\" rel=\"preload\" as=\"style\">" >> ../../app/templates/includes/base_vue_header.html
    echo "<link href=\"{{ url_for('static', filename='${flask_path}') }}\" rel=\"stylesheet\">" >> ../../app/templates/includes/base_vue_header.html

  done
}

function clear_inject_files() {
  git_sha=`git rev-parse --short HEAD`

  echo "" > ../../app/templates/includes/base_vue_header.html
  inject_git_version "../../app/templates/includes/base_vue_header.html" $git_sha

  echo "" > ../../app/templates/includes/base_vue_body.html
  inject_git_version "../../app/templates/includes/base_vue_body.html" $git_sha

  # also update the sha entry in dropdown menu
  echo "${git_sha}" > ../../app/templates/includes/git_short_sha.html
}

function update_menu_version_entry {
	git rev-parse --short HEAD > app/templates/includes/git_short_sha.html
}

# we migth also move this from makefile to here...
# function update_redactietool_version()


########### MAIN ROUTINE ##############

cd redactietool_widgets
compile_vue_components

echo -n "Updating vue includes in flask app..."
clear_inject_files
inject_css "dist/css"
inject_js "dist/js"
echo "done."


# to double check you could do this: 
# cd dist
# npm run serve

