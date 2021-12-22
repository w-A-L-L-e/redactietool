FROM python:3.9-slim

# Applications should run on port 8080 so NGINX can auto discover them.
EXPOSE 8080

# Make a new group and user so we don't run as root.
RUN addgroup --system appgroup && adduser -u 1001 --system appuser --ingroup appgroup

WORKDIR /app

# Let the appuser own the files so he can rwx during runtime.
COPY --chown=1001:0 . .
RUN  apt-get update &&  apt-get install -y --no-install-recommends  libxml2-dev libxmlsec1-dev libxmlsec1-openssl
# Install gcc and libc6-dev to be able to compile uWSGI
RUN set -ex; \
    build_deps='build-essential pkg-config' ;\
    apt-get install --no-install-recommends -y   $build_deps &&\
    /usr/local/bin/python -m pip install --upgrade pip setuptools wheel ; \
    pip install uWSGI==2.0.18 xmlsec>=1.0.5 ;\
    apt-get purge -y --auto-remove $build_deps && apt-get clean && rm -rf /var/lib/apt/lists/*   

USER appuser

# We install all our Python dependencies. Add the extra index url because some
# packages are in the meemoo repo.
RUN  pip install viaa-chassis==0.1.3 \
  --extra-index-url http://do-prd-mvn-01.do.viaa.be:8081/repository/pypi-internal/simple \
  --trusted-host do-prd-mvn-01.do.viaa.be &&\
  pip install -r requirements.txt --no-warn-script-location
ENV PATH=/home/appuser/.local/bin:$PATH   
# PLEASE use this only in the test keep main image clean
#    pip3 install -r requirements-test.txt && \
#    pip3 install flake8

#USER appuser

ENV OAS_JWT_SECRET ''
ENV OAS_SERVER 'https://oas-qas.viaa.be'
ENV OAS_APPNAME 'mediahaven'
ENV FLOWPLAYER_TOKEN 'set_in_secrets'


# This command will be run when starting the container. It is the same one that
# can be used to run the application locally.
ENTRYPOINT [ "uwsgi", "-i", "uwsgi.ini"]
