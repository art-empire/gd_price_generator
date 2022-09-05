import json
import os
import time

import pandas as pd
import numpy as np
import natsort
from slugify import slugify
from pathlib import Path

from .settings import *
from functools import reduce

import re


class PriceGenerator:
    data_frame = None
    time_stamp = time.time()
    media_path = None

    def _print_message(self, message='Прошло секунд.', old_time=None):
        new_time_stamp = time.time()
        old_time_stamp = old_time if old_time else self.time_stamp
        print('[%.5f] %s' % (new_time_stamp - old_time_stamp, message))

    def _init_data_frame(self, xls_file_config):
        self._print_message('Считываем файл %s.' % xls_file_config['file'])

        data_frame = None

        if xls_file_config['file'].suffix == '.csv':
            data_frame = pd.read_csv(
                xls_file_config['file'],
                sep='\t',
                usecols=xls_file_config['cols'].keys(),
                names=xls_file_config['cols'].values(),
                dtype=str,
                index_col=None,
                skiprows=xls_file_config['skip_rows']
            )

        elif xls_file_config['file'].suffix == '.xls':
            data_frame = pd.read_excel(
                io=xls_file_config['file'],
                sheet_name=xls_file_config['sheet'],
                usecols=xls_file_config['cols'].keys(),
                names=xls_file_config['cols'].values(),
                dtype=str,
                index_col=None,
                skiprows=xls_file_config['skip_rows']
            )
        else:
            print(xls_file_config['file'])
            print('- file format not supported')
            exit()

        # Заменяем NaN на 0
        data_frame.fillna(0, inplace=True)

        # Пропускаем строки в которых нет значений из колонок в списке
        for item in xls_file_config['skip_empty_fields']:
            data_frame = data_frame[data_frame[item] != 0]

        self._print_message('Обработан файл %s.' % xls_file_config['file'])

        return data_frame

    def get_int(self, value):
        res = str(value).strip()
        res = re.sub('[^0-9]', '0', res)
        return int(res or 0)

    def get_str(self, value):
        return str(value).strip()

    def get_bool(self, value):
        return 'Y' if value else 'N'

    def get_media_files_path(self, media_type='images'):
        self._print_message('Начинаем поиск файлов в ./%s/products/{brand}/{sku}/' % media_type)

        data_frame = pd.DataFrame(columns=['product_code', media_type])
        new_rows = np.array([])
        data = np.array([])

        media_files_count = 0
        not_found_list = []

        products_path = Path(media_type, 'products')

        pattern = './*.jpg' if media_type == 'images' else './*.*'

        for i, row in self.data_frame.iterrows():

            brand_product_code_path = Path(slugify(row.brand), self.get_str(row.product_code))
            file_path = self.media_path / products_path / brand_product_code_path
            media_files_list = natsort.natsorted(file_path.glob(pattern), alg=natsort.PATH)

            media_files = list(
                os.path.relpath(x, self.media_path) for x in media_files_list
            )
            media_files_count += 1
            if len(media_files) < 1:
                not_found_list.append(row.product_code)

            # print('%s: %s' % (row.product_code.ljust(20), list(str(os.path.relpath(x, file_path)) for x in media_files)))

            # new_row = {
            #     'Product Code': row.product_code,
            #     media_type.capitalize(): str('///'.join(media_files))
            # }

            new_row = {
                'product_code': row.product_code,
                media_type: str('///'.join(media_files))
            }

            data = np.append(data, np.array(new_row))

        data_frame = pd.DataFrame(list(data), columns=data_frame.columns)

        print(data_frame)

        self._print_message('Обработано %s артиклей' % media_files_count)
        if not_found_list:
            with open(BASE_DIR / 'out' / ('no_%s_list.txt' % media_type), 'w') as outfile:
                outfile.write("\n".join(not_found_list))
            self._print_message('У %s из них нет ни одного файла' % len(not_found_list))
            self._print_message('Список этих артиклей записан в ./out/no_%s_list.txt' % media_type)
        try:

            self.data_frame = self.data_frame.merge(data_frame, how='inner', on='product_code')
            # data_frame.to_csv(BASE_DIR / ('%s_files.csv' % media_type), encoding='utf-8', index=False, sep='\t')
            # self._print_message('Найденые медиа файлы сохранены в %s_files.csv' % media_type)
            self._print_message('Найденые медиа файлы сохранены')
        except:
            self._print_message('=====================================')
            self._print_message('| Не удалось записать  ./out/%s_files.csv |' % media_type)
            self._print_message('=====================================')

    def get_product_name(self, value):
        list = value.split('\n')
        name = self.get_str(list[0])
        effects = {
            'glow_in_the_dark': False,
            'glow_in_the_uv': False,
        }
        stickers = {
            'hit': False,
            'new': False,
            'sale': False,
        }

        list = list[1::]
        if len(list) > 0:
            effects_temp = self.get_str(list[0])
            if effects_temp.startswith('(') and effects_temp.endswith(')'):
                if effects_temp == '(Светится в темноте и ультрафиолете)':
                    effects['glow_in_the_dark'] = True
                    effects['glow_in_the_uv'] = True
                if effects_temp == '(Светится в темноте)':
                    effects['glow_in_the_dark'] = True
                if effects_temp == '(Светится в ультрафиолете)':
                    effects['glow_in_the_uv'] = True
                list = list[1::]
            list = ' '.join(list)
            for item in list.split(' '):
                if item == 'ХИТ!':
                    stickers['hit'] = True
                if item == 'NEW!':
                    stickers['new'] = True
                if item == 'SALE!':
                    stickers['sale'] = True

        return name, effects, stickers

    def get_main_price(self):

        def get_categories(a, b):
            m = ['%s///%s' % (x.strip(), y.strip()) for x in a for y in b]
            return '; '.join(m)

        self.data_frame['category'] = self.data_frame.apply(
            lambda row: get_categories(row.l1_category.split(';'), row.l2_category.split(';')), axis=1)
        self.data_frame['category_slug'] = self.data_frame.apply(
            lambda row: ' '.join([row.l1_category.split(';')[0], row.l2_category.split(';')[0]]), axis=1)

        data = np.array([])

        for i, row in self.data_frame.iterrows():

            name, effects, stickers = self.get_product_name(row.product_name)
            quantity = self.get_int(row.total_count)

            product_code = self.get_str(row.product_code)
            brand = self.get_str(row.brand)
            slug_brand = slugify(brand)

            images = self.get_str(row.images)
            video = json.dumps(list(filter(None, row.video.split('///'))))


            s = []
            stock = {}

            is_kids = 'Детское' in row.l1_category.split(';')

            for size in SIZES:
                if is_kids:
                    size_count = 0
                else:
                    size_count = self.get_int(row[size + '_size'])
                if size_count > 0:
                    s.append('%s' % size.upper())
                stock[size.upper()] = size_count

            for index, size in enumerate(SIZES_K):
                if is_kids:
                    size_count = self.get_int(row[SIZES[index] + '_size'])
                else:
                    size_count = 0
                if size_count > 0:
                    s.append('%s' % size.upper())
                stock[size.upper()] = size_count


            size_feature = '%s' % '///'.join(s)
            size_option = '(Gooood) Размер: SG[%s]' % ', '.join(list(set(SIZES + SIZES_K)))

            # s = []
            # stock = {}
            #
            # for idx, size in enumerate(SIZES):
            #     size_count = self.get_int(row[size + '_size'])
            #     if not ('Детское' in row.l1_category.split(';')):
            #         size_name = size.upper()
            #     else:
            #         size_name = SIZES_K[idx].upper()
            #         size_name = size.upper()
            #
            #     stock[size.upper()] = size_count
            #     s.append('%s' % size_name)
            #
            #
            # size_option = '(Gooood) Размер: SG[%s]' % ', '.join(s)
            #
            # s = []
            # stock = {}
            #
            # for idx, size in enumerate(SIZES):
            #     if not ('Детское' in row.l1_category.split(';')):
            #         size_name = size.upper()
            #     else:
            #         size_name = SIZES_K[idx].upper()
            #         size_name = size.upper()
            #
            #     size_count = self.get_int(row[size + '_size'])
            #     stock[size_name.upper()] = size_count
            #     if size_count > 0:
            #         s.append('%s' % size_name.upper())
            #
            # size_feature = '%s' % '///'.join(s)

            e = []
            if effects['glow_in_the_dark']:
                e.append('Светится в темноте')
            if effects['glow_in_the_uv']:
                e.append('Светится в ультрафиолете')

            effects_features = '%s' % '///'.join(e)

            new_row = {
                'Product Code': product_code,
                'Product name': name,
                'Category': self.get_str(row.category),
                'Quantity': quantity,
                'Price': self.get_int(row.price),
                'List price': self.get_int(row.list_price),
                'Цвет': self.get_str(row.color),
                'Бренд': brand,
                'Артикул': product_code,
                'Уход за вещами': self.get_str(row.product_care),
                'Пол': self.get_str(row.gender),
                'Страна': self.get_str(row.country),
                'Options': size_option,
                'Стикеры': json.dumps(stickers),
                'Размер для фильтров': size_feature,
                'Эффекты': effects_features,
                'Раздел': self.get_str(row.product_type),
                'Количество в наличии': json.dumps(stock),
                'Состав': self.get_str(row.consists),
                'Description': self.get_str(row.description_ru),
                'Images': images,
                'Video': video,
                'Add date': row.add_date,
                'Popularity': row.popularity,
            }
            data = np.append(data, np.array(new_row))

        res_df = pd.DataFrame(list(data))
        res_df.to_csv(BASE_DIR / 'out' / 'main_price.csv', encoding='utf-8', index=False, sep='\t')

    def get_opt_price(self):
        data = np.array([])
        for i, row in self.data_frame.iterrows():
            product_code = self.get_str(row.product_code)
            for key, value in USER_GROUPS.items():
                new_row = {
                    'Product code': product_code,
                    'Language': 'ru',
                    'Price': self.get_int(row[value['row']]),
                    'Lower limit': 1,
                    'User group': key,
                }
                data = np.append(data, np.array(new_row))

        res_df = pd.DataFrame(list(data))
        print(res_df)
        res_df.to_csv(BASE_DIR / 'out' / 'opt_price.csv', encoding='utf-8', index=False, sep='\t')

    def get_price(self):

        # Открываем каталоги и добавляем в лист
        df_list = []
        df_list.append(self._init_data_frame(xls_files_list['good_opt']))
        df_list.append(self._init_data_frame(xls_files_list['good_info']))

        # М склемваем их
        self.data_frame = reduce(lambda x, y: pd.merge(x, y, on='product_code'), df_list)

        # Вырезаем все не в наличии
        # self.data_frame = self.data_frame[self.data_frame.total_count != '0']

        # Ищем изображения
        self.get_media_files_path('images')
        self.get_media_files_path('video')

        self._print_message('Каталоги обьединены.')

        self.get_main_price()
        self._print_message('main_price.csv сгенерирован')

        self.get_opt_price()
        self._print_message('opt_price.csv сгенерирован')

    def __init__(self, media_path=BASE_DIR):
        self.data_frame = pd.DataFrame()
        self.media_path = media_path
