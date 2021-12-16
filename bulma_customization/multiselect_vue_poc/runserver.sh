#!/bin/bash
# Author: Walter Schreppers
cp ../dist/css/mystyles.css redactietool_widgets/public/
cp ../src/overrides.css redactietool_widgets/public/
cp ../src/modal_dialog.js redactietool_widgets/public/
cp ../dist/js/bundle.js redactietool_widgets/public/

cd redactietool_widgets
npm run serve

