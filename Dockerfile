FROM python:3.10-alpine

WORKDIR /app

COPY dist/ /app

RUN ls -la

RUN pip install geminal-*.tar.gz

ARG GOOGLE_API_KEY

ENV GOOGLE_API_KEY=$GOOGLE_API_KEY

CMD ["geminal"]
