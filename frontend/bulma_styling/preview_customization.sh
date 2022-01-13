#!/bin/bash
# Author: Walter Schreppers

echo "re-compiling bulma components"
./compile.sh

echo "Showing demo page with customized components..."
open index.html

echo "all done."

