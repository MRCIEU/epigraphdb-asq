import re
from typing import Optional

import html2text
import requests
from bs4 import BeautifulSoup
from pydash import py_

FULLTEXT_URL_TEMPLATE = "https://biorxiv.org/content/{uri}.full"

html_parser = html2text.HTML2Text(bodywidth=None)  # type: ignore
html_parser.ignore_links = True
html_parser.ignore_emphasis = True
html_parser.ignore_images = True
html_parser.ignore_tables = True


def get_full_text(doi: str, ver: int) -> str:
    uri = f"{doi}v{ver}"
    url = FULLTEXT_URL_TEMPLATE.format(uri=uri)
    r = requests.get(url)
    r.raise_for_status()
    res: str = r.content  # type: ignore
    return res


def find_fulltext(soup: BeautifulSoup) -> Optional[str]:
    search_res = soup.find("div", {"class": "article fulltext-view"})
    if not search_res:
        return None
    text = search_res.prettify()
    return text


def parse_to_text(html_text: str) -> str:
    return html_parser.handle(html_text)


def find_discussion_text(html_text: str) -> Optional[str]:
    soup = BeautifulSoup(html_text, "html.parser")
    # Remove sup reference tags
    for tag in soup(["sup"]):
        tag.decompose()
    # find all p-s under discussion and conclusion h2-s
    # NOTE: it won't find p-s under nested h3-s, might need hacks later
    h2 = soup.find_all(
        "h2", text=[re.compile("Discussion"), re.compile("Conclusion")]
    )
    para = py_.flatten([_.find_next_siblings("p") for _ in h2])
    if len(para) == 0:
        return None
    text_list = [parse_to_text(_.prettify()).strip() for _ in para]
    text = "\n".join(text_list)
    return text


def find_abstract_text(html_text: str) -> Optional[str]:
    soup = BeautifulSoup(html_text, "html.parser")
    # Remove sup reference tags
    for tag in soup(["sup"]):
        tag.decompose()
    h2 = soup.find_all("h2", text=[re.compile("Abstract")])
    para = py_.flatten([_.find_next_siblings("p") for _ in h2])
    if len(para) == 0:
        return None
    text_list = [parse_to_text(_.prettify()).strip() for _ in para]
    text = "\n".join(text_list)
    return text
