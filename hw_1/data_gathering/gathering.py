# -*- coding: utf-8 -*-
"""
ЗАДАНИЕ

Выбрать источник данных и собрать данные по некоторой предметной области.

Цель задания - отработать навык написания программ на Python.
В процессе выполнения задания затронем области:
- организация кода в виде проекта, импортирование модулей внутри проекта
- unit тестирование
- работа с файлами
- работа с протоколом http
- работа с pandas
- логирование

Требования к выполнению задания:

- собрать не менее 1000 объектов

- в каждом объекте должно быть не менее 5 атрибутов
(иначе просто будет не с чем работать.
исключение - вы абсолютно уверены что 4 атрибута в ваших данных
невероятно интересны)

- сохранить объекты в виде csv файла

- считать статистику по собранным объектам


Этапы:

1. Выбрать источник данных.

Это может быть любой сайт или любое API

Примеры:
- Пользователи vk.com (API)
- Посты любой популярной группы vk.com (API)
- Фильмы с Кинопоиска
(см. ссылку на статью ниже)
- Отзывы с Кинопоиска
- Статьи Википедии
(довольно сложная задача,
можно скачать дамп википедии и распарсить его,
можно найти упрощенные дампы)
- Статьи на habrahabr.ru
- Объекты на внутриигровом рынке на каком-нибудь сервере WOW (API)
(желательно англоязычном, иначе будет сложно разобраться)
- Матчи в DOTA (API)
- Сайт с кулинарными рецептами
- Ebay (API)
- Amazon (API)
...

Не ограничивайте свою фантазию. Это могут быть любые данные,
связанные с вашим хобби, работой, данные любой тематики.
Задание специально ставится в открытой форме.
У такого подхода две цели -
развить способность смотреть на задачу широко,
пополнить ваше портфолио (вы вполне можете в какой-то момент
развить этот проект в стартап, почему бы и нет,
а так же написать статью на хабр(!) или в личный блог.
Чем больше у вас таких активностей, тем ценнее ваша кандидатура на рынке)

2. Собрать данные из источника и сохранить себе в любом виде,
который потом сможете преобразовать

Можно сохранять страницы сайта в виде отдельных файлов.
Можно сразу доставать нужную информацию.
Главное - постараться не обращаться по http за одними и теми же данными много раз.
Суть в том, чтобы скачать данные себе, чтобы потом их можно было как угодно обработать.
В случае, если обработать захочется иначе - данные не надо собирать заново.
Нужно соблюдать "этикет", не пытаться заддосить сайт собирая данные в несколько потоков,
иногда может понадобиться дополнительная авторизация.

В случае с ограничениями api можно использовать time.sleep(seconds),
чтобы сделать задержку между запросами

3. Преобразовать данные из собранного вида в табличный вид.

Нужно достать из сырых данных ту самую информацию, которую считаете ценной
и сохранить в табличном формате - csv отлично для этого подходит

4. Посчитать статистики в данных
Требование - использовать pandas (мы ведь еще отрабатываем навык использования инструментария)
То, что считаете важным и хотели бы о данных узнать.

Критерий сдачи задания - собраны данные по не менее чем 1000 объектам (больше - лучше),
при запуске кода командой "python3 -m gathering stats" из собранных данных
считается и печатается в консоль некоторая статистика

Код можно менять любым удобным образом
Можно использовать и Python 2.7, и 3

Зачем нужны __init__.py файлы
https://stackoverflow.com/questions/448271/what-is-init-py-for

Про документирование в Python проекте
https://www.python.org/dev/peps/pep-0257/

Про оформление Python кода
https://www.python.org/dev/peps/pep-0008/


Примеры сбора данных:
https://habrahabr.ru/post/280238/

Для запуска тестов в корне проекта:
python3 -m unittest discover

Для запуска проекта из корня проекта:
python3 -m gathering gather
или
python3 -m gathering transform
или
python3 -m gathering stats


Для проверки стиля кода всех файлов проекта из корня проекта
pep8 .

"""

import logging

import sys
import pandas as pd
import numpy as np
from scrappers.scrapper import Scrapper
from parsers.parser import Parser
from storages.file_storage import FileStorage


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


SCRAPPED_FILE = 'ddelivery_points_data.json'
TABLE_FORMAT_FILE = 'ddelivery_points_data.csv'


def gather_process():
    logger.info("gather")
    storage = FileStorage(SCRAPPED_FILE)

    # You can also pass a storage
    scrapper = Scrapper()
    scrapper.scrap_process(storage)


def convert_data_to_table_format():
    logger.info("transform")
    storage = FileStorage(SCRAPPED_FILE)

    # transform gathered data from json file to pandas DataFrame and save as csv
    parser = Parser(storage)
    parser.parse(TABLE_FORMAT_FILE)


def stats_of_data():
    logger.info("stats")

    # Your code here
    # Load pandas DataFrame and print to stdout different statistics about the data.
    # Try to think about the data and use not only describe and info.
    # Ask yourself what would you like to know about this data (most frequent word, or something else)
    ddelivery_points = pd.read_csv('ddelivery_points_data.csv', index_col=None, header=0)
    ddelivery_points.head()


    print('Сколько наблюдений в наборе данных?')
    print(ddelivery_points.shape[0])

    print('Сколько наблюдений в наборе данных?')
    print(ddelivery_points.shape[1])


    print('Название столбцов:')
    print(ddelivery_points.columns)

    print('У какой компании больше точек доставки?')

    top_company_deliver_points = ddelivery_points[['delivery_company_name', 'id']]\
                                    .groupby('delivery_company_name')\
                                    .count().sort_values(by='id', ascending=False).reset_index()

    count_company = 15
    for delivery_company_name, index in zip(top_company_deliver_points.delivery_company_name, range(count_company)):
        if index > count_company:
            break
        print('Company name: {}'.format(delivery_company_name))

    print('У компании Call IM только одна точка доставки.')
    print('Вывести адресс этой точки доставки.')
    company_call_im = ddelivery_points[ddelivery_points.delivery_company_name == 'Call IM']

    for city_name, address, delivery_company_name in zip(company_call_im.city_name, company_call_im.address, company_call_im.delivery_company_name ):
        print(city_name, address, delivery_company_name)

    print('Топ городов по количеству пунктов самовывоза?')
    top_city = ddelivery_points[['city_id', 'city_name', 'delivery_company_id']].groupby(
        ['city_id', 'city_name']).count().sort_values(by='delivery_company_id', ascending=False).reset_index()

    count_company = 15
    for city_name, count, index in zip(top_city.city_name, top_city.delivery_company_id,  range(count_company)):
        if index > count_company:
            break
        print('Company name: {}  | Count of points: {}'.format(city_name, count))


    print('Сколько пунктов самовывоза в Краснодаре, которые принимают карты для оплаты?')

    card_pay_in_krasnodar = np.logical_and(ddelivery_points.city_id == 88, ddelivery_points.is_card == 1)
    print(ddelivery_points[card_pay_in_krasnodar].shape[0])


if __name__ == '__main__':
    """
    why main is so...?
    https://stackoverflow.com/questions/419163/what-does-if-name-main-do
    """
    logger.info("Work started")

    if sys.argv[1] == 'gather':
        gather_process()

    elif sys.argv[1] == 'transform':
        convert_data_to_table_format()

    elif sys.argv[1] == 'stats':
        stats_of_data()

    logger.info("work ended")
