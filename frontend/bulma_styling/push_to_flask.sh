#!/bin/bash
# Author: Walter Schreppers

echo "re-compiling bulma styling and components"
npm run build

echo -n "Updating flask core css and overrides and injecting into flask application app/static folder..."
cp -r dist/css/mystyles.css ../../app/static/bulma/core.css
cp src/overrides.css ../../app/static/bulma/overrides.css
cp dist/js/bundle.js ../../app/static/bulma/bundle.js
cp src/modal_dialog.js ../../app/static/bulma/modal_dialog.js

echo "all done."

