import logging
import random
import time
from datetime import datetime

from helpers import get_sftp_client, prepare_new_message_for_transfer
from paramiko import SFTPError
from prometheus_client import start_http_server

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    logger.info("Producer service started...")

    sftp_client = get_sftp_client()

    while True:
        try:
            local_file = prepare_new_message_for_transfer()

            remote_file = f"outbound/837/{local_file.name}".replace(
                ".edi", f"-{datetime.now().strftime('%s')}.edi"
            )

            sftp_client.put(local_file, remote_file)
            logger.info("SFTP transfer successful")
        except SFTPError as e:
            logger.error(f"SFTP transfer failed: {str(e)}")
        except Exception as e:
            logger.exception(f"Unexpected exception: {str(e)}")

        time.sleep(random.uniform(1.5, 10.0))  # seconds


if __name__ == "__main__":
    start_http_server(8000)
    main()
