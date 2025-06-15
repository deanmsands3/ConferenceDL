from .Conference import Conference
from . import defaults
import logging
import argparse


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Download MP3s of General Conference talks from the Church of Jesus Christ of Latter-day Saints "
                    "website.")
    parser.add_argument(
        "--base-url",
        default=defaults.BASE_URL,
        help="Base URL of the General Conference landing page (e.g., "
             "https://www.churchofjesuschrist.org/study/general-conference/2022/10?lang=eng)"
    )
    parser.add_argument(
        "--download-dir",
        default=defaults.DOWNLOAD_DIR,
        help="Directory to save downloaded MP3 files (default: general_conference_mp3s)"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=defaults.DELAY,
        help="Delay in seconds between requests to avoid overwhelming the server (default: 1.0)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output for debugging"
    )
    parsed_args = parser.parse_args()
    args_dict = {
        "base_url":parsed_args.base_url,
        "download_dir": parsed_args.download_dir,
        "delay": parsed_args.delay,
        "verbose": parsed_args.verbose
    }
    return args_dict


def cli_args(base_url: str, download_dir: str, delay: float, verbose: bool, *args, **kwargs) -> int:
    try:
        logging.basicConfig(
            level=(logging.INFO if verbose else logging.WARNING)
        )
        conference_talk_dl = Conference(base_url, download_dir, delay)
        conference_talk_dl.start()
        return 0
    except Exception as ex:
        logging.error(ex)
        return -1


def cli() -> int:
    args_dict = dict(parse_arguments())
    return cli_args(**args_dict)

if __name__ == '__main__':
    exit_code = cli()
    exit(exit_code)
