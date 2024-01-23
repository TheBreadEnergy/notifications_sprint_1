FROM python:3.11

WORKDIR /opt/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE 'config.settings'
ENV PIP_ROOT_USER_ACTION=ignore


RUN groupadd -r django && useradd -d /opt/app -r -g django django \
    && chown django:django -R /opt/app/

COPY app/requirements.txt requirements.txt
COPY app/uwsgi/uwsgi.ini uwsgi.ini

RUN apt-get update && apt-get install netcat-traditional && python -m pip install --upgrade pip && pip install -r requirements.txt --no-cache
COPY app/ .

RUN chmod +x docker-entrypoint.sh  && mkdir /opt/app/static && mkdir /opt/app/uploads


EXPOSE 8000

VOLUME /opt/app/static
VOLUME /opt/app/uploads

RUN chown -R django:django /opt/app/static
RUN chown -R django:django /opt/app/uploads

USER django
ENTRYPOINT ["/opt/app/docker-entrypoint.sh"]