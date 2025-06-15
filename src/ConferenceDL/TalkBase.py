from bs4 import BeautifulSoup

from .SessionBase import SessionBase

class TalkBase(object):
    _talk_title: str
    _soup: BeautifulSoup
    _parent: SessionBase
    _talk_url: str
    def __init__(self, parent: SessionBase, talk_url:str):
        self._parent = parent
        self._talk_url = talk_url

    @property
    def parent(self) -> SessionBase:
        return self._parent

    @property
    def talk_url(self) -> str:
        return self._talk_url

    @property
    def talk_title(self):
        return self._talk_title

    @talk_title.setter
    def talk_title(self, value: str):
        self._talk_title = value

    @property
    def soup(self) -> BeautifulSoup:
        return self._soup

    @soup.setter
    def soup(self, value):
        self._soup = value
