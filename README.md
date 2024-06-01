# Проект парсинга pep

## Описание

Проект включает 4 парсера:

1. Whats-new
cобирает информацию о заголовке, авторе и ссылке для каждой версии Python на странице [Что нового в Питоне?](https://docs.python.org/3/whatsnew/).
2. Latest-versions
берет [Ссылку документации](https://docs.python.org/3/), номер версии и статус для каждой версии Python на главной странице документации.
3.  Download
скачивает PDF-архив для каждой версии Python на странице [Скачивания документации](https://docs.python.org/3/download.html).
4. Pep
собирает статус и ссылку для каждого [документа PEP](https://peps.python.org/), сравнивает статусы и подсчитывает количество документов в каждом статусе.


## Используемые технологии 

* Python 3.9.10
    * requests-cache (v 1.0.0)
    * tqdm (v 4.61.0)
    * beautifulsoup4 (v 4.9.3)



## Как запустить проект

Клонировать репозиторий, создать и активировать venv:
```
git clone git@github.com:dxndigiden/bs4_parser_pep.git
python -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```
Перейти в папку с проектом:
```
cd bs4_parser_pep/src
```
Запустить парсер с обязательным аргументом mode (whats-new|latest-versions|download|pep)
```
python main.py {mode}
```
Опциональные аргументы:
```
-c, --clear-cache                          Очистка кеша
-o {pretty,file}, --output {pretty,file}   Изменяет вывод данных (pretty-табличка в консоль или csv-файл)
```

## Автор: [Денис Смирнов](https://github.com/dxndigiden)