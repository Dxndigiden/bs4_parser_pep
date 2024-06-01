from collections import defaultdict
import logging
import re
from urllib.parse import urljoin

import requests_cache
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (
    BASE_DIR,
    MAIN_DOC_URL,
    MAIN_PEPS_URL,
    EXPECTED_STATUS,
    DOWNLOADS_DIR
)
from exceptions import ParserFindTagException, ElementsNotFoundExeption
from outputs import control_output
from utils import find_tag, ready_soup


def whats_new(session):

    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    soup = ready_soup(session, whats_new_url)
    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all(
        'li',
        attrs={'class': 'toctree-l1'}
        )
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    for section in tqdm(sections_by_python, desc='парcинг пошел'):
        version_a_tag = find_tag(section, 'a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)
        soup = ready_soup(session, version_link)
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append((version_link, h1.text, dl_text))
    return results


def latest_versions(session):

    soup = ready_soup(session, MAIN_DOC_URL)
    sidebar = find_tag(soup, 'div', attrs={'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
        else:
            raise ElementsNotFoundExeption('Ничего не нашлось.')
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        link = a_tag['href']
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append((link, version, status))
    return results


def download(session):

    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    soup = ready_soup(session, downloads_url)
    main_tag = find_tag(soup, 'div', attrs={'role': 'main'})
    table_tag = find_tag(main_tag, 'table', attrs={'class': 'docutils'})
    pdf_a4_tag = find_tag(table_tag, 'a',
                          attrs={'href': re.compile(r'.+pdf-a4\.zip$')})
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / DOWNLOADS_DIR
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(f'Архив был загружен и сохранён: {archive_path}')


def pep(session):

    soup = ready_soup(session, MAIN_PEPS_URL)
    tr_tags = soup.select('#numerical-index tbody tr')
    statuses = defaultdict(int)
    unexpected_statuses = []
    errors = []
    for tr_tag in tqdm(tr_tags):
        try:
            status_in_table = EXPECTED_STATUS[find_tag(tr_tag, 'td').text[1:]]
            pep_url = urljoin(
                MAIN_PEPS_URL, find_tag(
                    tr_tag, 'a', {'class': 'pep reference internal'}
                )['href']
            )
            soup = ready_soup(session, pep_url)
        except ConnectionError as error:
            errors.append(f'Обрабатывая {pep_url} появилась ошибка {error}')
            continue
        except ParserFindTagException as error:
            errors.append(f'{error} на {pep_url}')
            continue
        status_in_cart = soup.find(
            string='Status'
        ).find_parent('dt').find_next_sibling().text
        if status_in_cart not in status_in_table:
            unexpected_statuses.append(
                f'{pep_url}\nСтатус в: {status_in_cart}'
                f'\nОжидаемые статусы: {status_in_table}'
                )
        statuses[status_in_cart] += 1
    if errors:
        logging.error('\n'.join(errors))
    if unexpected_statuses:
        logging.error(f'Несовпадающие статусы:\n{unexpected_statuses}')
    return [
        ('Статус', 'Количество'),
        *statuses.items(),
        (('Total:'), sum(statuses.values())),
    ]


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():

    configure_logging()
    logging.info('Парсер запущен!')
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')
    try:
        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()
        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)
        if results is not None:
            control_output(results, args)
        logging.info('Парсер завершил работу.')
    except Exception as error:
        logging.exception(f'Парсер завершил работу c ошибкой!\n{error}',
                          stack_info=True
                          )


if __name__ == '__main__':
    main()
