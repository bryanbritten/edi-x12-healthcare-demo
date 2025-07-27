FROM python:3.11-slim
WORKDIR /consumer
COPY consumer.py /consumer/consumer.py
RUN pip install --no-cache-dir prometheus-client
EXPOSE 8000
CMD ["python", "consumer.py"]