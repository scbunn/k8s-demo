FROM python:3-alpine
LABEL maintainer="stephen.bunn@avalara.com"
EXPOSE 5000

RUN mkdir -p /usr/local/k8s 
RUN apk --no-cache add postgresql-dev gcc python3-dev musl-dev && \
    pip install psycopg2-binary && \
    apk del gcc python3-dev musl-dev

COPY docker-entrypoint.sh /
WORKDIR /usr/local/k8s

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    chmod +x /docker-entrypoint.sh

COPY app.py .

RUN python app.py

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["k8s"]
