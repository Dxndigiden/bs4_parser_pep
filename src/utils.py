from bs4 import BeautifulSoup
import logging
from requests import RequestException

from exceptions import ParserFindTagException, ParserResponseException


def get_response(session, url, encoding='utf-8'):

    try:
        response = session.get(url)
        response.encoding = encoding
        return response
    except RequestException as error:
        raise ParserResponseException(
            f'Ошибка при загрузке страницы {url}\n{error}',
            stack_info=True
            )


def find_tag(soup, tag, attrs=None):

    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag


def ready_soup(session, url, features='lxml'):
    return BeautifulSoup(get_response(session, url).text, features=features)
