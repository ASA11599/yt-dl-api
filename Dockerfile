FROM python:3.9.0rc1-alpine3.12

WORKDIR /app

COPY ./api.py .

RUN apk add youtube-dl

EXPOSE 80

CMD ["python3", "api.py"]
