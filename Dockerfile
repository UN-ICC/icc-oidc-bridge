###########
# BUILDER #
###########

# pull official base image
FROM python:3.9.9-slim as builder

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc \
    python3-psycopg2 apache2 apache2-dev

# install python dependencies
RUN pip install --upgrade pip ; \
    pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels mod_wsgi newrelic

COPY requirements.txt .
COPY requirements_dev.txt .

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.9.9-slim

# install psycopg2 dependencies
RUN apt-get update && apt-get install -y python3-psycopg2 \
    apache2 poppler-utils && rm -rf /var/lib/apt/lists/*

RUN addgroup --system app && useradd --system --create-home --gid app --shell /bin/false app

# create the appropriate directories
ENV APP_HOME=/code
RUN mkdir $APP_HOME $APP_HOME/static && chown app:app -R $APP_HOME
WORKDIR $APP_HOME
ENV PATH="/home/app/.local/bin:${PATH}"

# change to the app user
USER app

# install dependencies
COPY --chown=app:app --from=builder /usr/src/app/wheels /wheels
COPY --chown=app:app --from=builder /app/requirements.txt .

RUN pip install --upgrade pip ; \
    pip install --no-cache /wheels/*

# copy project
COPY --chown=app:app . $APP_HOME

EXPOSE 8080
CMD ["/code/start.sh"]