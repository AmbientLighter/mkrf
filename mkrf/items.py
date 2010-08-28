#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

def field(s):
    f = Field()
    f['txt'] = s
    return f

class FilmItem(Item):
    title = field('Название')
    genre = field('жанр')
    firm = field('Фирма')
    country = field('страна')
    year = field('год выпуска')
    dubbed = field('дубляж')
    category = field('категория')
    orig_language = field('язык оригинала')
    orig_title = field('языке оригинала')
    format = field('формат')
    series = field('серий')
    colour = field('Цветной')
    parts = field('Частей')
    footage = field('Метраж')
    duration = field('Длительность')
    limitation = field('граничения')
    producer = field('Продюссер')
    scenario = field('Сценарист')
    director = field('Режиссер')
    composer = field('Композитор')
    operator = field('Оператор')
    artist = field('Художник')
    note = field('Примечание')
    annotation = field('Аннотация')
    id = Field()
    blocked = Field()
    
class LicenseItem(Item):
    lic_num = field('Номер прокатного удостоверения')
    lic_date = field('Дата прокатного удостоверения')
    cat = field('Категория прав проката')
    exp = field('Окончание прав проката')
    add = field('Описание прав проката')
    firm = field('Фирма заявитель')
    tel = field('Телефон фирмы Заявителя')
    num = field('Номер договора')
    date_beg = field('Дата заключения договора')
    date_end = field('Дата заполнения')
    id = Field()
