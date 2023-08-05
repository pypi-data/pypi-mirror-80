import argparse
import getpass
import logging
import platform
import sys
from pathlib import Path

from .config import load_config
from .worker import Worker

logger = logging.getLogger()


def main(discoset, hostname, username, target_directory):
    config = load_config(discoset)
    host = config.get_host(hostname)
    user = host.get_user(username)
    logger.debug("Got items: %s", user.items)

    source_directory = discoset.parent.resolve()
    worker = Worker(source_directory, target_directory, user.items)
    if worker.is_valid():
        if worker.warnings:
            logger.info("Warnings: %s", worker.warnings)
        worker.execute()
        return worker.warnings
    else:
        raise Exception(worker.errors)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", action="store_true")
    parser.add_argument("--discoset", default=Path("./Discoset"), type=Path)
    parser.add_argument("--hostname", type=str, default=platform.node())
    parser.add_argument("--username", type=str, default=getpass.getuser())
    parser.add_argument("--target-directory", type=Path, default=Path.home())
    args = parser.parse_args()
    return args


# Used as entrypoint by setuptools
def _main():
    args = parse_arguments()
    args = vars(args)
    if args.pop("v"):
        # Get root logger and set level
        logging.getLogger().setLevel(logging.INFO)
    logger.debug("Got args: %s", args)
    main(**args)
