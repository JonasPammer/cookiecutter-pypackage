# syntax=docker/dockerfile:1.4
FROM python:3.11-slim-bullseye
LABEL maintainer="{{ cookiecutter.email }}"
LABEL org.opencontainers.source="https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}"

ARG DOCKER_APP_USER=secureappuser
ARG DOCKER_APP_DIR=/app
ARG VIRTUAL_ENV=${DOCKER_APP_DIR}/venv

### General Debian Docker Best-Practice Preperation Steps ###
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# upgrade system packages (for security purposes) and install tini
USER root
RUN export DEBIAN_FRONTEND=noninteractive && apt-get -qy update \
    && apt-get -qy upgrade \
    && apt-get -qy install --no-install-recommends tini \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create non-root user for security purposes
# (https://github.com/hexops/dockerfile#run-as-a-non-root-user)
USER root
RUN if [ "${DOCKER_APP_USER}" != "root" ]; then \
        addgroup --gid 10001 --system "${DOCKER_APP_USER}" \
        && adduser --uid 10000 --system --ingroup "${DOCKER_APP_USER}" --home "/home/${DOCKER_APP_USER}" "${DOCKER_APP_USER}"; \
    fi

# create app dir
USER root
RUN mkdir -p "${DOCKER_APP_DIR}" \
    && chown -R "${DOCKER_APP_USER}:${DOCKER_APP_USER}" "${DOCKER_APP_DIR}"

### General Python Debian Docker Best-Practice Preperation Steps ###
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# install python3-wheel and (for security purposes) upgrade python packages of system python
USER root
RUN export DEBIAN_FRONTEND=noninteractive && apt-get -qy update \
    && apt-get -qqy install --no-install-recommends python3-wheel \
    && python3 -m pip install --no-cache-dir --upgrade pip \
    && python3 -m pip install --no-cache-dir --upgrade setuptools \
    && python3 -m pip install --no-cache-dir --upgrade wheel \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# create venv and alter ENV's for all subsequent calls (like 'source venv/bin/active' would do)
USER root
RUN python3 -m venv "${VIRTUAL_ENV}" \
    && chown -R "${DOCKER_APP_USER}:${DOCKER_APP_USER}" "${DOCKER_APP_DIR}"
ENV VIRTUAL_ENV=${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# upgrade python packages of venv python
USER ${DOCKER_APP_USER}
RUN true \
    && python3 -m pip install --no-cache-dir --upgrade pip \
    && python3 -m pip install --no-cache-dir --upgrade setuptools \
    && python3 -m pip install --no-cache-dir --upgrade wheel


### Project-Specific Dockerfile Steps ###
WORKDIR ${DOCKER_APP_DIR}

COPY --chown="${DOCKER_APP_USER}:${DOCKER_APP_USER}" requirements.txt .
USER ${DOCKER_APP_USER}
RUN python3 -m pip install --no-cache-dir -r requirements.txt --require-hashes

COPY --chown="${DOCKER_APP_USER}:${DOCKER_APP_USER}" . .
USER ${DOCKER_APP_USER}
RUN python3 -m pip install --no-cache-dir  .


### Configure Container Startup Configuration ###
WORKDIR ${DOCKER_APP_DIR}
USER ${DOCKER_APP_USER}

# (Tini allows us to avoid several Docker edge cases,
#  see https://github.com/krallin/tini / https://hynek.me/articles/docker-signals/)
ENTRYPOINT [ "/usr/bin/tini", "--",  "{{ cookiecutter.pkg_name }}" ]

# Default arguments for the ENTRYPOINT go in CMD (https://github.com/hexops/dockerfile#only-store-arguments-in-cmd)
#CMD ["--foo", "1"]
