import re
import typing

import mechanicalsoup


def login(username: str, password: str) -> mechanicalsoup.StatefulBrowser:
    browser = mechanicalsoup.StatefulBrowser()
    browser.open("https://flightaware.com/account/session")
    browser.select_form('form[action="https://flightaware.com/account/session"]')
    browser["flightaware_username"] = username
    browser["flightaware_password"] = password
    browser.submit_selected()
    return browser


def get_history_page(
    browser: mechanicalsoup.StatefulBrowser, target: str, offset: str = None
) -> typing.Tuple[typing.List[str], typing.Optional[str]]:
    url = f"https://flightaware.com/live/flight/{target}/history"
    if offset:
        url += f"/{offset}"
    browser.open(url)
    page = browser.get_current_page()
    history_re = re.compile(r"^/live/flight/[^/]+/history/(\d+)/?")
    urls = []
    next_page = None
    for link in page.select("td a"):
        href = link.attrs.get("href", "")
        if match := history_re.match(href):
            if len(num := match.group(1)) >= 8:
                urls.append(f"https://flightaware.com{href}")
            elif len(num) >= 2:
                next_page = num
    return urls, next_page


def get_all_history(browser: mechanicalsoup.StatefulBrowser, target: str):
    urls, next_page = get_history_page(browser, target)
    while next_page is not None:
        more_urls, next_page = get_history_page(browser, target, offset=next_page)
        urls += more_urls
    return urls
