# Vue framework for building custom widgets in the metadata form

We start of with a working minimal vue app.
We'll be stripping/minifying this also (if we decide to go this route).

This allows us to quickly prototype some multi select widgets with custom views for the template and 
tagging parts in our metadata form.

Quick starting point : https://medium.com/quick-code/how-to-create-a-simple-vue-js-app-in-5-minutes-f74fb04adc01
Also showing how to use axios in order to make some ajax requexts (which we'll mostl likely use with some routes
to our flask app that under the hood use the suggest library from Miel to query the knowledge graph).



Run following scripts, first install vue with npm:

```
$ ./install_vue.sh
```

Then generate a clean vue app (choose npm and defaults for babel+eslint):

```
$ ./create_vue_widgets_app.sh
Creating minimal vue redactietool frontend app for our selector components...
For now just choose default babel/eslinter and NPM as package manager:
You are using Node v13.14.0.
Node.js 13.x has already reached end-of-life and will not be supported in future major releases.
It's strongly recommended to use an active LTS version instead.


Vue CLI v4.5.15
? Please pick a preset: Default ([Vue 2] babel, eslint)


Vue CLI v4.5.15
✨  Creating project in /Users/wschrep/FreelanceWork/VIAA/redactietool/bulma_customization/multiselect_vue_poc/redactietool_widgets.
⚙️  Installing CLI plugins. This might take a while...


> fsevents@1.2.13 install /Users/wschrep/FreelanceWork/VIAA/redactietool/bulma_customization/multiselect_vue_poc/redactietool_widgets/node_modules/watchpack-chokidar2/node_modules/fsevents
> node install.js
...
```

Now start the dev server to quickly prototype the vue components:

```
$ ./devserver.sh

> redactietool_widgets@0.1.0 serve /Users/wschrep/FreelanceWork/VIAA/redactietool/bulma_customization/multiselect_vue_poc/redactietool_widgets
> vue-cli-service serve

 INFO  Starting development server...

....

 App running at:
  - Local:   http://localhost:8081/
  - Network: http://192.168.0.215:8081/

```


This allows to quickly develop the vue components in the browser (with live reload).

When you're done run this script which makes a production ready build of the components and injects it into the flask application:

```
$ ./deploy_to_app.sh
DONE  Compiled successfully in 3328ms                                             4:51:47 PM

  File                                   Size                     Gzipped

  dist/js/chunk-vendors.fd3d1052.js      138.53 KiB               46.88 KiB
  dist/js/app.1b4c739b.js                18.13 KiB                4.73 KiB
  dist/modal_dialog.js                   2.06 KiB                 0.67 KiB
  dist/bundle.js                         0.34 KiB                 0.24 KiB
  dist/mystyles.css                      188.28 KiB               25.40 KiB
  dist/css/chunk-vendors.ac5b10c9.css    7.29 KiB                 1.71 KiB
  dist/css/app.a0114f2a.css              1.23 KiB                 0.45 KiB
  dist/overrides.css                     0.22 KiB                 0.16 KiB

  Images and other types of assets omitted.

 DONE  Build complete. The dist directory is ready to be deployed.
 INFO  Check out deployment instructions at https://cli.vuejs.org/guide/deployment.html

 Updating vue includes in flask app... done.
```


