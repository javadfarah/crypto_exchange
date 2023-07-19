FROM dockerhub.charisma.tech/python:3.9-slim
LABEL maintainer="Mohammadjavad Farahnak"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive
ADD odbcinst.ini /etc/
RUN apt-get update -y && apt-get install -y curl gnupg
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update -y && apt-get install -y unixodbc unixodbc-dev tdsodbc freetds-common freetds-bin freetds-dev
RUN apt-get update && ACCEPT_EULA=Y apt-get -y install mssql-tools msodbcsql18
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
RUN export DJANGO_SETTINGS_MODULE=core.settings
COPY requirements.txt /tmp/requirements.txt
RUN pip --timeout=1000 install -i https://pypi.iranrepo.ir/simple  --no-cache-dir -r /tmp/requirements.txt
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
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
#CMD ["/start.sh"]
