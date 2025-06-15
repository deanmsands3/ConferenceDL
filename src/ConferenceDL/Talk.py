import logging
from urllib.parse import urljoin
import re
from pathlib import Path
from bs4 import Tag
from typing import Any
import base64
import json
from .TalkBase import TalkBase
from .SessionBase import SessionBase


class Talk(TalkBase):
    WINDOW_INITIAL_STATE_RE = re.compile(r'window\.__INITIAL_STATE__="(.+)"')
    CHURCH_ASSETS_CDN = "https://assets.churchofjesuschrist.org/"

    def __init__(self, parent: SessionBase, talk_url: str):
        super().__init__(parent, talk_url)

    def _find_window_initial_state_json(self) -> Any | None:
        """
        Find a script tage containing the window.__INITIAL_STATE__ declaration.
        Decode the Base64 into JSON.
        Parse the JSON.
        """
        script: Tag = self.soup.find("script", text=Talk.WINDOW_INITIAL_STATE_RE)
        if not script:
            return None
        window_initial_state_b64 = Talk.WINDOW_INITIAL_STATE_RE.match(script.text).group(1)
        windows_initial_state_json = base64.b64decode(window_initial_state_b64)
        windows_initial_state = json.loads(windows_initial_state_json)
        return windows_initial_state

    def get_mp3_url(self):
        """Extract the MP3 download URL from a talk page."""
        windows_initial_state = self._find_window_initial_state_json()
        if not windows_initial_state:
            return None
        content_store: dict = windows_initial_state["reader"]["contentStore"]
        talk_id_obj = list(content_store.values())[0]
        audio_list = talk_id_obj["meta"]["audio"]
        # Find the audio download link
        audio_sources = [audio["mediaUrl"] for audio in audio_list if audio["variant"] == "audio"]
        if not audio_sources:
            return None

        mp3_url = str(audio_sources[0])
        if not mp3_url.startswith('http'):
            mp3_url = urljoin(Talk.CHURCH_ASSETS_CDN, mp3_url)
        return mp3_url

    def save_metadata(self, filepath):
        metadata = {"title": self.talk_title, "session": self.parent.session_name, "url": self.talk_url}
        with open(f"{filepath}.json", "w") as f:
            json.dump(metadata, f, indent=2)

    def download_mp3(self, mp3_url):
        """Download the MP3 file and save it with a sanitized filename."""
        # Sanitize the talk title and session name for the filename
        safe_title = re.sub(r'[^\w\s-]', '', self.talk_title).strip().replace(' ', '_')
        safe_session = re.sub(r'[^\w\s-]', '', self.parent.session_name).strip().replace(' ', '_')
        filepath = Path(self.parent.download_dir) / f"{safe_session}_{safe_title}.mp3"
        self.parent.download_file(mp3_url, str(filepath.resolve()))

    def process(self):
        """Process talk page HTML then JSON to extract MP3 URL"""
        # Extract talk title
        self.soup = self.parent.fetch_soup(self.talk_url)
        self.talk_title = "Unknown_Talk"
        if not self.soup:
            raise f"Could not parse {self.talk_url}"
        title_tag = self.soup.find('h1')
        if title_tag:
            self.talk_title = title_tag.text.strip()

        logging.info(f"Processing talk: {self.talk_title}")

        # Get MP3 URL
        mp3_url = self.get_mp3_url()
        if mp3_url:
            self.download_mp3(mp3_url)
        else:
            logging.error(f"No MP3 found for talk: {self.talk_title}")
