FROM python:3.6

ARG APP_USER=app
RUN groupadd -r ${APP_USER} && useradd -m -g ${APP_USER} ${APP_USER} 

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update && apt-get install -y python3-psycopg2 apache2 apache2-dev

# copy project
RUN mkdir /code
WORKDIR /code

RUN chown app:app /code

USER app
ENV PATH="/home/app/.local/bin:${PATH}"

COPY requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt
RUN pip install mod_wsgi

COPY . /code

EXPOSE 8080
CMD ["/code/start.sh"]