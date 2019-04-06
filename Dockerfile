FROM python:2.7
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt 
COPY ./app /app
RUN chmod +x /app/* \
    && ls /app
WORKDIR /app

CMD ["/app/tx-dns-update.sh"]
