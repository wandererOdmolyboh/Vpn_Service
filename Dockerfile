FROM python:3.12

ENV PYTHONUNBUFFERED 1
RUN mkdir /src

COPY requirements/requirements_docker.txt .
RUN pip install -r requirements_docker.txt

COPY docker/app.sh .
RUN chmod +x /app.sh

COPY .env /src

COPY /src /src

CMD ["/app.sh"]