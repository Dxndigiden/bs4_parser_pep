import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import (BASE_DIR,
                       DT_FORMAT_FOR_FILE,
                       PRETTY_OUTPUT,
                       FILE_OUTPUT
                       )


def default_output(results, cli_args):

    for row in results:
        print(*row)


def pretty_output(results, cli_args):

    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args):

    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DT_FORMAT_FOR_FILE)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, dialect='unix')
        writer.writerows(results)
    logging.info(f'Файл с результатами был сохранён: {file_path}')


OUTPUT_METHODS = {
    PRETTY_OUTPUT: pretty_output,
    FILE_OUTPUT: file_output,
    None: default_output,
}


def control_output(results, cli_args):

    return OUTPUT_METHODS[cli_args.output](results, cli_args)
