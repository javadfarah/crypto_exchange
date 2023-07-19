FROM python:3.9-slim
LABEL maintainer="Mohammadjavad Farahnak"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive
RUN export DJANGO_SETTINGS_MODULE=core.settings
COPY requirements.txt /tmp/requirements.txt
RUN pip --timeout=1000 install  -i https://pypi.iranrepo.ir/simple  --no-cache-dir -r /tmp/requirements.txt
COPY ./start.sh /start.sh
RUN chmod +x /start.sh
COPY ./gunicorn_conf.py /gunicorn_conf.py
COPY . /app
WORKDIR /app/src
ENV PYTHONPATH=/app
EXPOSE 80

#ENTRYPOINT ["/entrypoint.sh"]

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn
CMD ["/start.sh"]
