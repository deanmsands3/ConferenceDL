import logging
import time
import os
import requests
from typing import List
from bs4 import BeautifulSoup, Tag, PageElement
from pathlib import Path
from .ConferenceBase import ConferenceBase
from .Session import Session


class Conference(ConferenceBase):
    # Base URL for the General Conference (example: October 2022)
    BASE_URL = "https://www.churchofjesuschrist.org/study/general-conference/2022/10?lang=eng"
    # Directory to save MP3 files
    DOWNLOAD_DIR = "general_conference_mp3s"
    # User-Agent for requests
    HEADERS = {
        "User-Agent": "ConferenceTalkDL/0.1.0 (contact: deanmsands3@gmail.com)"
    }

    def __init__(self,
                 base_url: str = BASE_URL, download_dir: str = DOWNLOAD_DIR,
                 delay: float = 1.0, headers=None
                 ):
        if headers is None:
            headers = Conference.HEADERS
        download_path = Path(download_dir).resolve()
        if not download_path.is_dir():
            download_path.mkdir(parents=True, exist_ok=True)
        safe_download_dir = str(download_path)
        super().__init__(base_url, safe_download_dir, delay, headers)
        self.soup = self.fetch_soup(self.base_url)
        if not self.soup:
            raise f"Could not process html data at {self.base_url}"

    def start(self) -> None:
        """
            Initiate the scraping and downloading process for all sessions in the conference.

            Creates the download directory if it doesn't exist, fetches session links, and processes each session.
        """
        # Create download directory if it doesn't exist
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
            logging.info(f"Created download directory: {self.download_dir}")

        logging.info(f"Scraping General Conference: {self.base_url}")

        # Get session links
        session_list_items = self.find_session_list()
        if not session_list_items:
            logging.warning("No session list items found.")
            return

        for session_list_item in session_list_items:
            self._process_session(session_list_item)
            # Be polite: add a small delay to avoid overwhelming the server
            self.nap_between_sessions()

    def find_session_list(self) -> List[PageElement]:
        page_div = self.soup.find("div", id="page")
        app_div = page_div.find("div", id="app")
        main = app_div.find("main")
        toc_section: Tag = main.div.section
        toc_div: Tag = toc_section.div
        toc_nav: Tag = toc_div.find("nav")
        items_ul: Tag = toc_nav.ul
        session_list: List[PageElement] = list(items_ul.children)[1:]
        return session_list

    def _process_session(self, session_list_item):
        session = Session(self, session_list_item)
        session.process()

    def fetch_soup(self, url):
        """Fetch and parse a webpage using BeautifulSoup."""
        response = self.cached_session.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')

    def download_file(self, file_url: str, filepath: str, no_overwrite: bool = True):
        """Downloads a file to disk"""
        # Check if the file exists
        if os.path.exists(filepath) and no_overwrite:
            logging.info(f"File {filepath} already exists, skipping download.")
            return
        # Attempt to download the file
        try:
            response = self.cached_session.get(file_url, stream=True)
            response.raise_for_status()
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            logging.info(f"Downloaded: {filepath}")
        except requests.ConnectionError:
            logging.error(f"Connection error downloading {file_url}")
            return
        except requests.Timeout:
            logging.error(f"Timeout downloading {file_url}")
            return
        except requests.RequestException as e:
            logging.error(f"Error downloading {file_url}: {e}")

    def nap_between_sessions(self):
        """Simple delay so as not to overwhelm the Church's website"""
        time.sleep(self.delay)
