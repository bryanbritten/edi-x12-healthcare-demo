FROM python:3.11-slim
WORKDIR /invalidator
COPY invalidator.py /invalidator/invalidator.py
RUN pip install --no-cache-dir prometheus-client
EXPOSE 8000
CMD ["python", "invalidator.py"]