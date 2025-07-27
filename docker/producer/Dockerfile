FROM python:3.11-slim
WORKDIR /producer
COPY docker/producer/data/ /producer/data/
COPY .env /producer/.env
COPY docker/producer/helpers.py /producer/helpers.py
COPY docker/producer/producer.py /producer/producer.py

RUN <<EOF
mkdir data/wrapped
mkdir data/wrapped/999
mkdir data/wrapped/277
mkdir data/wrapped/834
mkdir data/wrapped/835
mkdir data/wrapped/837
mkdir data/wrapped/837/Institutional
mkdir data/wrapped/837/Professional
mkdir data/wrapped/837/Dental
EOF

RUN pip install --no-cache-dir paramiko prometheus-client python-dotenv
EXPOSE 8000
CMD ["python", "producer.py"]