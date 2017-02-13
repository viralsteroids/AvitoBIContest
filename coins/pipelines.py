# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re

class FindDate(object):

    not_date_formats = (
        r'(?i)(?:номер|отдельно|тираж)\s*?\D{0,10}\s*?(?:1[123456789]\d{2})(?:\b|\D)',  # номер 30
        r'(?i)\b(?:грамм?|гр\.|gr\.?|gramm?e?|мм\.?|штук)\s*?[:=-]?\s*?(?:1[123456789]\d{2}|20[01]\d)(?:\b|\D)',  # мм. 30
        r'(?i)(?:\b|\D)(?:1[123456789]\d{2})\D{0,5}(?:номер|тираж|экземпляр|мм\b|грам|гр\.|gr)',  # 30 номер
        r'(?i)(?:\b|\D)(?:1[123456789]\d{2}|20[01]\d)\s*?(?:р\b|руб\b|рубл|₽|долл?ар|евро|doll?ar|euro|\$|€)', # 1000 рублей
        r'(?i)(?:\b|\D)(?:1[123456789]\d{2}|2000)\s*?[:=-]?\s*?(?:лет|монет|мон\b|шт\.?(?:\b|\D)|штук|за шт|за монету|за мон\b)', # 200 лет
        r'(?i)Вес\D{0,10}(?:1[123456789]\d{2}|20[01]\d)(?:\b|\D)',  # Вес около 700
        r'(?i)Вес\D{0,10}\d{2,4}\s*?-\s*?(?:1[123456789]\d{2}|20[01]\d)(?:\b|\D)',  # Вес около 70-800г.
        r'(?i)(?:войн|сражен)[а-я]{0,5}\s*?1812',  # в войне 1812 года
    )

    certain_date_formats = (
        r'(?i)(?:\b|\D)([3456789]\d{2})\s*?-\s*?1?[123456789]\d{2}\s*?(?:год)',  # 957-978 года
        r'(?i)(?:\b|\D)([3456789]\d{2})\s*?(?:год)',  # 992 года
        r'(?i)(?:\b|\D)(1[123456789]\d{2}|20[01]\d)\s*?(?:г[.\s]|гг|год)',  # 1957г.
        r'(?i)(?:\b|\D)(1[123456789]\d{2})\s*?-\s*?(?:1\d{3}|20[01]\d|\d{2})(?:\b|\D)',  # 1957-2003
        r'(?i)(?:\b|\D)(20[01]\d)\s*?-\s*?(?:20[01]\d|\d{2})(?:\b|\D)',  # 2003-2017
        r'(?i)(?:выпуск[а-я]*?|чекан[а-я]*?|произв[а-я]*?|дата)\D{0,20}(?:(?:\d{1,2}[.-\/|]){0,2}|\d{1,2}\s*?[А-Яа-я]+?\.?\s*?)(1[123456789]\d{2}|20[01]\d)', # Дата выпуска: 01.10.2013
        r'(?i)дата(?:\s*?[а-я]+?)?\s*?[:=\—-]\s*?(1[123456789]\d{2}|20[01]\d)(?:\b|\D)',  # Дата: 1957
    )

    probable_date_formats = (
        r'(?:\b|\D)(1[123456789]\d{2})(?:\b|\D)',  # 1537
        r'(?:\b|\D)(20[01]\d)(?:\b|\D)',  # 2007
        r'(?:\b|\D)(1[123456789]\d{2}|[3456789]\d{2})\s*?-\s*?\d{2}(?:\b|\D)',  # 867-88
    )

    dates_to_convert_short = (
        r'(?i)(?:\b|\D)([123456789]{2})\s*?-\s*?[123456789]{2}\s*?год',  # 92-93 года
        r'(?i)(?:\b|\D)([123456789]{2})\s*?год',  # 93 год
    )

    dates_to_convert_century = (
        r'(?i)(?:\b|\D)(1[0123456789])\s*?-\s*?(?:1[123456789]|20)\s*?(?:век|вв?\.?(?:\b|\D))',  # 19-20в
        r'(?i)(?:\b|\D)(1[0123456789]|20)\s*?век',  # 19век
    )

    dates_to_convert_roman_century = (
        r'(?i)(?:\b|\D)(I|II|III|IIII|IV|V|VI|VII|VIII|VIII|IIX|IX|X|XI|XII|XIII|XIIII|XIV|XV|XVI|XVII|XVIII|XIIX|XIX|XX)\s*?-\s*?(?:I|II|III|IIII|IV|V|VI|VII|VIII|VIII|IIX|IX|X|XI|XII|XIII|XIIII|XIV|XV|XVI|XVII|XVIII|XIIX|XIX|XX)\s*?(?:век|вв?\.?(?:\b|\D))', # XIX-XX
        r'(?i)(?:\b|\D)(I|II|III|IIII|IV|V|VI|VII|VIII|VIII|IIX|IX|X|XI|XII|XIII|XIIII|XIV|XV|XVI|XVII|XVIII|XIIX|XIX|XX)\s*?век', # XIXвек
    )


    def process_item(self, item, spider):
        area_search = item['title'] + (' ! ' + item['description'] if 'description' in item else '')

        # Clean area_search by not_date_formats
        for regex in self.not_date_formats:
            area_search = re.sub(regex, ' ', area_search)

        # Parse certain dates
        certain_dates = []
        for regex in self.certain_date_formats:
            certain_dates += [(int(match.start()), int(match.group(1))) for match in re.finditer(regex, area_search)]

        # Parse and convert short dates
        short_dates = []
        for regex in self.dates_to_convert_short:
            short_dates += [(int(match.start()), match.group(1)) for match in re.finditer(regex, area_search)]
        short_dates = [(date[0], int('19' + date[1])) for date in short_dates if date]

        # Parse and convert century dates
        century_dates = []
        for regex in self.dates_to_convert_century:
            century_dates += [(int(match.start()), match.group(1)) for match in re.finditer(regex, area_search)]
        century_dates = [(date[0], int('19' + date[1])) for date in century_dates if date]

        # Parse and convert roman century dates
        roman_century_dates = []
        for regex in self.dates_to_convert_roman_century:
            roman_century_dates += [(int(match.start()), match.group(1)) for match in re.finditer(regex, area_search)]
        roman_numerals = {'I': 99,
                          'II': 199,
                          'III': 299,
                          'IIII': 399,
                          'IV': 399,
                          'V': 499,
                          'VI': 599,
                          'VII': 699,
                          'VIII': 799,
                          'IIX': 799,
                          'IX': 899,
                          'X': 999,
                          'XI': 1099,
                          'XII': 1199,
                          'XIII': 1299,
                          'XIIII': 1399,
                          'XIV': 1399,
                          'XV': 1499,
                          'XVI': 1599,
                          'XVII': 1699,
                          'XVIII': 1799,
                          'XIIX': 1799,
                          'XIX': 1899,
                          'XX': 1999,
                          }
        roman_century_dates = [(int(date[0]), int(roman_numerals[date[1]])) for date in roman_century_dates if date]

        dates = certain_dates + short_dates + century_dates + roman_century_dates

        # Parse probable dates
        if not dates:
            probable_dates = []

            for regex in self.probable_date_formats:
                probable_dates += [(int(match.start()), int(match.group(1))) for match in re.finditer(regex, area_search)]
            dates = probable_dates

        if dates:
            item['date'] = int(min(dates, key=lambda x: x[0])[1])
        else:
            item['date'] = None

        return item