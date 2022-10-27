FROM python:3.10-alpine
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
COPY ./app /app

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip3 install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh entrypoint.sh
RUN sed -i 's/\r$//g' entrypoint.sh
RUN chmod +x entrypoint.sh

# create the app user
RUN addgroup -S app && adduser -S app -G app

WORKDIR /app

# change to the app user
USER app

ENTRYPOINT ["sh", "/entrypoint.sh"]