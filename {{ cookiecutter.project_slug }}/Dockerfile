FROM python:3.7-slim-bullseye

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
    && apt-get -qy install --no-install-recommends apt-utils tini \
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

# Create and use non-root user for security purposes (https://github.com/hexops/dockerfile#run-as-a-non-root-user)
RUN addgroup --gid 10001 --system secureappuser \
 && adduser  --uid 10000 --system --ingroup secureappuser --home /home/secureappuser secureappuser
USER secureappuser

WORKDIR /app
COPY . .
RUN pip3 install .

### Configure Container Startup Configuration ###

# (Tini allows us to avoid several Docker edge cases, see https://github.com/krallin/tini)
ENTRYPOINT [ "/usr/bin/tini", "--",  "{{ cookiecutter.pkg_name }}" ]

# Default arguments for the ENTRYPOINT go in CMD (https://github.com/hexops/dockerfile#only-store-arguments-in-cmd)
#CMD ["--foo", "1"]