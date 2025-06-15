from bs4 import BeautifulSoup
import requests_cache

class ConferenceBase(object):
    _soup: BeautifulSoup
    _base_url: str
    _download_dir: str
    _delay: float
    _cached_session: requests_cache.CachedSession

    def __init__(self,
                 base_url: str, download_dir: str,
                 delay: float = 1.0, headers: dict = None
                 ):
        self._base_url = base_url
        self._download_dir = download_dir
        self._delay = delay
        self._cached_session = requests_cache.CachedSession(cache_name='conference_cache')
        self._cached_session.headers.update(headers or {})

    def start(self) -> None:
        pass

    def fetch_soup(self, url) -> BeautifulSoup:
        """Fetch and parse a webpage using BeautifulSoup."""
        pass

    def download_file(self, file_url: str, filepath: str, no_overwrite: bool = True) -> None:
        """Downloads a file to disk"""
        pass

    def nap_between_sessions(self) -> None:
        """Simple delay so as not to overwhelm the Church's website"""
        pass

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def download_dir(self) -> str:
        return self._download_dir

    @property
    def delay(self) -> float:
        return self._delay

    @property
    def soup(self) -> BeautifulSoup:
        return self._soup

    @soup.setter
    def soup(self, value):
        self._soup = value

    @property
    def cached_session(self) -> requests_cache.CachedSession:
        return self._cached_session