from bs4 import BeautifulSoup, Tag
from .ConferenceBase import ConferenceBase


class SessionBase(object):
    _session_name: str
    _soup: Tag
    _parent: ConferenceBase
    _soup: Tag
    def __init__(self, parent: ConferenceBase, list_item_element:Tag):
        self._parent: ConferenceBase = parent
        self._soup: Tag = list_item_element

    def process(self):
        pass

    def fetch_soup(self, url:str) -> BeautifulSoup:
        return self.parent.fetch_soup(url)

    @property
    def parent(self) -> ConferenceBase:
        return self._parent

    @property
    def soup(self) -> Tag:
        return self._soup

    @soup.setter
    def soup(self, value):
        self._soup = value

    @property
    def session_name(self):
        return self._session_name

    @session_name.setter
    def session_name(self, value):
        self._session_name = value

    @property
    def download_dir(self):
        return self.parent.download_dir

    def download_file(self, file_url: str, filepath: str, no_overwrite: bool = True):
        self.parent.download_file(file_url, filepath, no_overwrite)
