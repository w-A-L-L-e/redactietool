#!/bin/bash
# Author: Walter Schreppers
cp ../dist/css/mystyles.css redactietool_widgets/public/
# overrides.css will be customized further here to build the lom sections
# cp ../src/overrides.css redactietool_widgets/public/
cp ../src/modal_dialog.js redactietool_widgets/public/
cp ../dist/js/bundle.js redactietool_widgets/public/

cd redactietool_widgets
npm run serve

