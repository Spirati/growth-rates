FROM python:latest

WORKDIR /bot

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN export SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt

COPY . .

CMD ["python", "bot.py"]