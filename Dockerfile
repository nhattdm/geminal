FROM python:3.9-alpine

WORKDIR /root

COPY . .

RUN pip install . 

ARG GOOGLE_API_KEY

ENV GOOGLE_API_KEY=$GOOGLE_API_KEY

CMD ["geminal"]