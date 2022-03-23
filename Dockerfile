FROM python:3.8-alpine as builder

ENV LANG C.UTF-8

# This is our runtime
RUN ln -sf /usr/bin/pip3 /usr/bin/pip
RUN ln -sf /usr/bin/python3 /usr/bin/python

# This is dev runtime
RUN apk add --no-cache --virtual .build-deps build-base python3-dev
RUN apk add --no-cache libffi-dev gcc musl-dev make
# Using latest versions, but pinning them
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install --no-cache-dir pipenv==2018.10.13

# This is where pip will install to
ENV PYROOT /pyroot
# A convenience to have console_scripts in PATH
ENV PATH $PYROOT/bin:$PATH

ENV PYTHONUSERBASE $PYROOT

# THE MAIN COURSE #
WORKDIR /build

# Install dependencies
COPY Pipfile Pipfile.lock ./

RUN PIP_USER=1 PIP_IGNORE_INSTALLED=1 pipenv install --system --deploy
# Install our application
COPY . ./

RUN pip install --user .

####################
# Production image #
####################
FROM python:3.8-alpine AS prod
# This is our runtime, again
# It's better be refactored to a separate image to avoid instruction duplication
RUN ln -sf /usr/bin/pip3 /usr/bin/pip
RUN ln -sf /usr/bin/python3 /usr/bin/python
#! Comment after debugging
RUN apk add --no-cache bash
ENV PYROOT /pyroot
ENV PATH $PYROOT/bin:$PATH
ENV PYTHONPATH $PYROOT/lib/python:$PATH
# This is crucial for pkg_resources to work
ENV PYTHONUSERBASE $PYROOT

# In most cases we don't need entry points provided by other libraries
COPY --from=builder $PYROOT/bin/TA $PYROOT/bin/

# Finally, copy artifacts
COPY --from=builder $PYROOT/lib/ $PYROOT/lib/
#TODO Update Workdir with you project folder name
WORKDIR /pyroot/lib/python3.8/site-packages/Tiktok_Analytics

