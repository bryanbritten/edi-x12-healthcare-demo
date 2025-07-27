import logging

from prometheus_client import start_http_server

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s %(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Consumer service started...")

if __name__ == "__main__":
    start_http_server(8000)
    main()