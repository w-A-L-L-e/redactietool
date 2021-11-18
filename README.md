# Redactie tool

## Synopsis
Upload form for subtitles as collateral for mediaobject and editing metadata using calls
to knowledge graph. Searches by pid. Shows overview page with selection to either edit metadata
or upload new subtitle file. Shows flowplayer with subtitles after you upload a valid srt.
Subtitle srt is converted to webvtt for pre-viewing in flowplayer.
Finally submit to mediahaven (show confirmation dialog if a srt is already linked).
Allows basically to upload both closed and open srt files to videos for 'testbeeld' tenant
(tenant is now only one but can be easily extended for multiple tenants).

## Prerequisites

* Git
* Docker
* Python 3.6+
* Linux (if you want to run it locally, uwsgi is not available on other platforms.)
* Access to the meemoo PyPi

## Usage

1. Clone this repository with:

    `$ git clone https://github.com/viaacode/redactietool.git`

2. Change into the new directory.

### Running locally

There is a Makefile included now. If you run make without arguments you can
see all available commands:

```
$ make
Available make commands:

  install               install packages and prepare environment
  clean                 remove all temporary files
  lint                  run the code linters
  format                reformat code
  test                  run all the tests
  coverage              run tests and generate coverage report
  server                start uvicorn development server and serve application locally
  debug                 start server in debugging mode for auto restarting after code changes etc.
  dockerrun             run docker image and serve web application in docker
                        (normally only needed if there are deploy issues)
  preview               Preview changed assets before copying into flask
  precompile_assets     re-compile bulma core.css, overrides.css and 
                        place into flask application assets folder
```

1. Start by running make install which installs the pip packages and sets up the environment.

2. Start the server in debug mode like so:

```
$ make debug
__________           .___              __  .__         ___________           .__   
\______   \ ____   __| _/____    _____/  |_|__| ____   \__    ___/___   ____ |  |  
 |       _// __ \ / __ |\__  \ _/ ___\   __\  |/ __ \    |    | /  _ \ /  _ \|  |  
 |    |   \  ___// /_/ | / __ \\  \___|  | |  \  ___/    |    |(  <_> |  <_> )  |__
 |____|_  /\___  >____ |(____  /\___  >__| |__|\___  >   |____| \____/ \____/|____/
        \/     \/     \/     \/     \/             \/                              

                 Develop mode, running on http://localhost:8080 


 * Serving Flask app "app.redactietool" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
{"message": " * Running on http://127.0.0.1:8080/ (Press CTRL+C to quit)"}
{"message": " * Restarting with stat"}
{"message": " * Debugger is active!"}

```


3. Run the tests with:

    `$ make test`

5. To run the web application in production mode use this make command :

   `$ make server`

The application is now serving requests on `localhost:8080`. Try it with:

    `$ curl -v -X GET http://127.0.0.1:8080/`

Or just visit this url in your browser http://127.0.0.1:8080

### Running using Docker

1. Build the container and run it:

   `$ make dockerrun`

### Helper scripts
To run the tests locally and also run flake8 linter/code checking:
```

$ make test    
===================================== test session starts ======================================
platform darwin -- Python 3.9.7, pytest-5.4.1, py-1.10.0, pluggy-0.13.1 -- /Users/wschrep/FreelanceWork/VIAA/subloader/python_env/bin/python
cachedir: .pytest_cache
rootdir: /Users/wschrep/FreelanceWork/VIAA/redactietool
plugins: recording-0.11.0, cov-2.8.1, mock-3.5.1
collected 29 items                                                                             

tests/test_app.py::test_home PASSED                                                      [  3%]
tests/test_app.py::test_liveness_check PASSED                                            [  6%]
tests/test_app.py::test_search_media_security PASSED                                     [ 10%]
tests/test_app.py::test_search_media PASSED                                              [ 13%]
tests/test_app.py::test_invalid_pid_entry PASSED                                         [ 17%]
tests/test_app.py::test_empty_pid PASSED                                                 [ 20%]
tests/test_app.py::test_wrong_pid_entry PASSED                                           [ 24%]
tests/test_app.py::test_working_pid_search PASSED                                        [ 27%]
tests/test_app.py::test_bad_srt_upload PASSED                                            [ 31%]
tests/test_app.py::test_invalid_upload PASSED                                            [ 34%]
tests/test_app.py::test_empty_upload PASSED                                              [ 37%]
tests/test_app.py::test_valid_subtitle PASSED                                            [ 41%]
tests/test_app.py::test_valid_subtitle_capitals PASSED                                   [ 44%]
tests/test_app.py::test_cancel_upload PASSED                                             [ 48%]
tests/test_app.py::test_subtitle_videoplayer_route PASSED                                [ 51%]
tests/test_app.py::test_subtitle_videoplayer_route_unknownfile PASSED                    [ 55%]
...

tests/test_sidecar.py::test_sidecar_v2 PASSED                                            [100%]
================================= 25 passed in 1.63s =================================
Running flake8 linter...
ALL OK
```
If you get flake8 warnings during development there's a scripts/autopep command you can run
that will auto-fix most styling issues (basically a python equivalent to rubocop -a used in ruby projects).


### Tests code coverage

Test coverage report can be generated with following coverage makefile command:

```
$ make coverage
Name                          Stmts   Miss  Cover
-------------------------------------------------
app/__init__.py                   0      0   100%
app/authorization.py             50     24    52%
app/config.py                    19      0   100%
app/ftp_uploader.py              30      7    77%
app/mediahaven_api.py            54     10    81%
app/redactietool.py             243     95    61%
app/subtitle_files.py           146      3    98%
app/validation.py                35      6    83%
debug.py                          3      3     0%
list_videos.py                    8      8     0%
tests/__init__.py                 2      0   100%
tests/conftest.py                 9      0   100%
tests/fixtures.py                21      0   100%
tests/test_app.py               172      0   100%
tests/test_authorization.py      31      0   100%
tests/test_sidecar.py            14      0   100%
wsgi.py                           3      3     0%
-------------------------------------------------
TOTAL                           840    159    81%
Coverage HTML written to dir htmlcov
```

Then you can open the generated test coverage report here:
```
open htmlcov/index.html
```

### Environment variables

Best set following environment variables before running the server. This
allows login to work and also makes the mediahaven calls to upload the srt and lookup
metadata by pid functional:

```
export MEDIAHAVEN_API=https://archief-qas.viaa.be/mediahaven-rest-api
export MEDIAHAVEN_USER= lookup in team pass
export MEDIAHAVEN_PASS= lookup in team pass

export OAS_SERVER=https://oas-qas.viaa.be
export OAS_APPNAME=mediahaven

export FLOWPLAYER_TOKEN= lookup or ask Bart or Walter for this token
```

For production deploys you also set the OAS_JWT_SECRET (see last section on verification of bearer token). Flowplayer token is also needed to be able to preview the subtitles in the flow player (on dev/localhost it works without token,but once deployed you need it to not get an error from the player).
This env var is exposed to javascript code starting flowplayer in app/templates/preview.html


### Running the server locally:

To run a server on port 8080:

```
$ make server
```
The root page is now a login screen that both supports a form based login and a one button/saml authentication
which shares your login with other Meemoo applications.

following this link <a href="http://127.0.0.1:8080/">Redactietool localhost</a> after you have the server running.


During development you can autoformat and check linting errors like so:
```
$ make lint
```

Auto reformatting (a lot like rubocop but then with python):
```
$ make format
```


### Updating the bulma styling

To keep inline with most of our other web applications. A new makefile command called precompile_assets was added.
This recompiles the bulma sass files with your customized variables and then places this in the correct location in the
flask application static assets folder:

```
$ make precompile_assets
cd bulma_customization && ./push_to_flask.sh
re-compiling bulma components

> bulma_latest_version@0.9.3 build /Users/wschrep/FreelanceWork/VIAA/redactietool/bulma_customization
> webpack --mode production

asset css/mystyles.css 169 KiB [compared for emit] (name: main)
asset js/bundle.js 349 bytes [compared for emit] [minimized] (name: main)
Entrypoint main 170 KiB = css/mystyles.css 169 KiB js/bundle.js 349 bytes
orphan modules 172 KiB (javascript) 937 bytes (runtime) [orphan] 7 modules
runtime modules 274 bytes 1 module
cacheable modules 79 bytes (javascript) 169 KiB (css/mini-extract)
  javascript modules 79 bytes
    ./src/index.js 29 bytes [built] [code generated]
    ./src/mystyles.scss 50 bytes [built] [code generated]
  css modules 169 KiB
    css ./node_modules/css-loader/dist/cjs.js!./node_modules/sass-loader/dist/cjs.js??ruleSet[1].rules[0].use[2]!./src/mystyles.scss 68 bytes [built] [code generated]
    css ./node_modules/css-loader/dist/cjs.js!./node_modules/sass-loader/dist/cjs.js??ruleSet[1].rules[0].use[2]!./src/mystyles.scss (1) 169 KiB [built] [code generated]
webpack 5.64.1 compiled successfully in 1236 ms
updating flask core css and overrides...
all done.
```

### Verification of bearer token

In order to verify bearer token the secret key is shared. This is base64 encode hs256 jwt key. We share the key as environment variable OAS_JWT_SECRET
and it is stored here for qas: https://do-prd-okp-m0.do.viaa.be:8443/console/project/public-api/browse/secrets/avo-oas-qas-develop-config
and here for prd: https://do-prd-okp-m0.do.viaa.be:8443/console/project/public-api/browse/secrets/avo-oas-prd-master-config.

The k value for the respective environment is stored in OAS_JWT_SECRET and the syncrator-api decodes + verifies the jwt signature from OAS in the verify_token method in app/authorization.py we also verify the audience == 'syncrator' this is the 'aud' in the jwt token. When signature verification is enabled this verifies also the audience and throws an exception if it does not match (which is caught and results in a 401 access denied). Without the OAS_JWT_SECRET a fallback mode decodes the jwt token and checks the 'aud' value but this is unsecure and therefore a warning message will be printed to setup the secret properly.

However this above bearer and oas_jwt will soon become deprecated as we will fully switch to SAML authentication once this is up and running on the QAS instance of the 'Ondertitel en redactie tool'


### Dislaimer regarding pytest pyvcr recordings.
For integration tests with other services like Mediahaven API and oas server logins we use pytest-recording pip package.
If you want to rerecord the automated request responses used in some tests you can do so by deleting the yaml files in tests/cassettes.
If you write new tests be sure to also filter out the authorization headers. Before this was done/configured we accidentally exposed a basic auth header in all
generated yaml files (and this contains the pasword that is stored in normally an env var or secret because the header can be decoded).

To filter out headers in recorded api responses best use this snippet:
```
@pytest.fixture(scope="module")
def vcr_config():
    return {
        "record_mode": "once",
        "filter_headers": ["authorization"]
    }
```
