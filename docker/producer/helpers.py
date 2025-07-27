import glob
import os
import random
from datetime import datetime
from pathlib import Path

import paramiko
from dotenv import load_dotenv
from paramiko import SFTPClient

load_dotenv()


# In production, you may want to code defensively and use `.get()`
# This is a toy project, so I am confident the values will be there
SFTP_CONFIG = {
    "host": os.environ["SFTP_HOST"],
    "port": int(os.environ["SFTP_PORT"]),
    "username": os.environ["SFTP_USERNAME_HOSPITAL_SENDER"],
    "password": os.environ["SFTP_PASSWORD_HOSPITAL_SENDER"],
}


def get_sftp_client() -> SFTPClient:
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(
        SFTP_CONFIG["host"],
        SFTP_CONFIG["port"],
        SFTP_CONFIG["username"],
        SFTP_CONFIG["password"],
    )
    return ssh_client.open_sftp()


def get_random_file() -> Path:
    # TODO: expand beyond 837 messages
    all_files = glob.glob("data/raw/837/*/*.edi")
    return Path(random.choice(all_files))


def chunk_into_transaction_sets(segments: list[str]) -> list[str]:
    """
    Takes a list of segments and buckets them into Transaction Sets.

    Args:
        segments (list[str]): One or more segments representing the data in the X12 document

    Returns
        list[str]: A list of Transaction Segments represented as a single string
    """

    transaction_sets = []
    cur_transaction_set = ""
    for segment in segments:
        if not segment:
            continue

        cur_transaction_set += f"{segment}\n"
        if segment.startswith("SE*"):
            transaction_sets.append(cur_transaction_set)
            cur_transaction_set = ""

    return transaction_sets


def wrap_in_functional_group(
    transaction_sets: list[str],
    sender_id: str = "123456789",
    receiver_id: str = "987654321",
    control_number: str = "1",
    functional_id_code: str = "HC",
    version: str = "005010X",
    document_number: str = "222",
    addenda: str = "A1",
    separator: str = "*",
) -> str:
    """
    Wraps one or more Transaction Sets into a Functional Group

    Args:
        transaction_sets (list[str]): A list of Transaction Sets
        sender_id (str): The ID of the sending entity
        receiver_id (str): The ID of the receiving entity
        control_number (str): The Interchange Control Number. Will be 0-padded to 9 digits.

    Returns:
        str: A Functional Group containing one or more Transaction Sets
    """

    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    date, time = timestamp[:8], timestamp[8:]
    n = len(transaction_sets)
    full_version = f"{version}{document_number}{addenda}"

    gs_segment = separator.join(
        [
            "GS",
            functional_id_code,
            sender_id,
            receiver_id,
            date,
            time,
            control_number.zfill(9),
            "X",
            full_version,
            "~",
        ]
    )
    ge_segment = f"GE*{n}*{control_number}~"
    transaction_sets_str = "\n".join(transaction_sets)
    return f"{gs_segment}\n{transaction_sets_str}\n{ge_segment}"


def wrap_in_interchange_envelope(
    functional_group: str,
    sender_id: str = "123456789",
    receiver_id: str = "987654321",
    control_number: str = "1",
) -> str:
    """
    Wraps a Functional Groups in an Interchange Envelope

    Args:
        functional_groups (list[str]): One ore more Functional Groups, each containing one or more Transaction Sets
        sender_id (str): The ID of the sending entity
        receiver_id (str): The ID of the receiving entity
        control_number (str): The Interchange Control Number. Will be 0-padded to 9 digits.

    Returns:
        str: A full X12 Interchange Envelope message
    """
    timestamp = datetime.now().strftime("%y%m%d%H%M")
    date, time = timestamp[:6], timestamp[6:]
    sender_id = sender_id.ljust(15)
    receiver_id = receiver_id.ljust(15)

    isa_segment = (
        f"ISA*00*          *00*          *ZZ*{sender_id}*ZZ*{receiver_id}"
        f"*{date}*{time}*^*00501*{control_number.zfill(9)}*0*T*:~"
    )
    iea_segment = f"IEA*1*{str(control_number).zfill(9)}~"

    return f"{isa_segment}\n{functional_group}\n{iea_segment}"


def prepare_new_message_for_transfer() -> Path:
    """
    Randomly selects a message from a repo of example messages and wraps the Transaction Sets
    into a Functional Group and then into an Interchange Envelope. It then saves the message
    back to disk and returns the file path where it was stored.

    Args:
        outpath (Path): Filepath where the final message should be stored.

    Returns:
        Path: The file path where the wrapped message is saved.
    """

    local_file = get_random_file()
    outpath = Path(str(local_file).replace("raw", "wrapped"))

    with open(local_file, "r") as f:
        segments = f.readlines()

    functional_group = wrap_in_functional_group(segments)
    interchange_envelope = wrap_in_interchange_envelope(functional_group)

    with open(outpath, "w") as f:
        f.write(interchange_envelope)

    return outpath
