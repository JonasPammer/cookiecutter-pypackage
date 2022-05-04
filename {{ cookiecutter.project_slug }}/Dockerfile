FROM python:3.7-slim-buster

LABEL maintainer="{{ cookiecutter.email }}"
LABEL org.label-schema.schema-version="1.0"
LABEL org.label-schema.vcs-url="https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}"

### General Python Debian Docker Best-Practice Preperation Steps ###
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -qy update \
    && apt-get -qy install --no-install-recommends apt-utils=1.* \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV=/app
RUN python3 -m venv "${VIRTUAL_ENV}"
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

RUN apt-get -qy update \
    && apt-get -qqy install python3-wheel \
    && pip3 install --no-cache-dir --upgrade pip \
    && pip3 install --no-cache-dir wheel \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

### Install Project ###
WORKDIR /app
COPY . .
RUN pip3 install .

### Configure Container Startup Configuration ###
#ENTRYPOINT [ "/bin/bash" ]
ENTRYPOINT [ "python" "-m" "{{ cookiecutter.pkg_name }}" ]