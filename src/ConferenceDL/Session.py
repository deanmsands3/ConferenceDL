import logging
import re
from urllib.parse import urljoin
from bs4 import Tag
from .ConferenceBase import ConferenceBase
from .SessionBase import SessionBase
from .Talk import Talk


class Session(SessionBase):
    TALK_LINKS_RE = re.compile(r'.*/\d{4}/\d{2}/[a-z0-9-]+(\?lang=[a-z]+)?$')

    def __init__(self, parent: ConferenceBase, list_item_element: Tag):
        super().__init__(parent, list_item_element)

    def process(self):
        # Extract session name from URL or page
        title_tag: Tag = self.soup.a.div.p.span
        self.session_name = title_tag.text.strip() if title_tag else "Unknown_Session"

        logging.info(f"\nProcessing session: {self.session_name} ({self.session_name})")

        # Get talk links for the session
        talk_links = self.get_talk_links()
        if not talk_links:
            logging.error(f"No talk links found for session: {self.session_name}!")
            return
        for talk_url in talk_links:
            self._process_talk(talk_url)

    def get_talk_links(self):
        """Extract individual talk links from a session page element."""
        talk_links = []
        talks_ul: Tag = self.soup.ul

        # Find the list of talks (based on page structure)
        talks_list_items = list(talks_ul.find_all("li"))
        if not talks_list_items:
            return []
        for talk_list_item in talks_list_items:
            link = talk_list_item.find('a', href=True)
            href = link['href']
            # Check if it's a talk page (contains a number or specific pattern)
            if Session.TALK_LINKS_RE.match(href):
                full_url = urljoin(self.parent.base_url, href)
                talk_links.append(full_url)

        return talk_links

    def _process_talk(self, talk_url: str):
        talk = Talk(self, talk_url)
        talk.process()
