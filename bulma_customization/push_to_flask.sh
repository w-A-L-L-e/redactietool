#!/bin/bash
# Author: Walter Schreppers

echo "re-compiling bulma components"
./compile.sh

echo "updating flask core css and overrides..."
cp -r dist/css/mystyles.css ../app/static/bulma/core.css
cp src/overrides.css ../app/static/bulma/overrides.css

echo "all done."

