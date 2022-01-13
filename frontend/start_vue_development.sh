#!/bin/bash
# Author: Walter Schreppers

echo "Bringing customized bulma to vue..."
cp bulma_styling/dist/css/mystyles.css redactietool_widgets/public/
cp bulma_styling/src/modal_dialog.js redactietool_widgets/public/
cp bulma_styling/dist/js/bundle.js redactietool_widgets/public/

echo "Firing up vue dev server..."
cd redactietool_widgets
npm run serve

