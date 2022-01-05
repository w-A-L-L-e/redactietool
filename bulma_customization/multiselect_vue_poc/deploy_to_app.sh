#!/bin/bash

cd redactietool_widgets
npm run build

# cd dist
# npm run serve

# move newly compiled widgets into flask app (and remove old ones)
rm -rf ../../../app/static/vue/*
cp -r dist/css ../../../app/static/vue
cp -r dist/js ../../../app/static/vue
