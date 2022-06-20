#!/usr/bin/env python3

import pandas as pd
import numpy as np
from slugify import slugify
from pathlib import Path

import time
import natsort

import json

from src.main import PriceGenerator


def init_main():
    start_time = time.time()
    print('Считываем основной каталог.')

    opt_cols = {
        0: 'product_code',
        2: 'product_name',
        3: 'product_type',
        4: 'brand',
        5: 'l1_category',
        6: 'l2_category',
        7: 'color',
        8: 'consists',
        9: 'price',
        10: 'list_price',

        11: 'small_opt_price',
        13: 'opt_price',
        14: 'price-3',
        15: 'price-7',
        16: 'price-11',
        17: 'price-10',
        18: 'price-15',
        19: 'price-20',
        20: 'price-22',
        21: 'price-25',

        23: 'total_count',
        24: 'ns_size',
        25: '3xs_size',
        26: '2xs_size',
        27: 'xs_size',
        28: 's_size',
        29: 'm_size',
        30: 'l_size',
        31: 'xl_size',
        32: '2xl_size',
        33: '3хl_size',
        34: '4хl_size',
        35: '5xl_size',
    }

    df_opt = pd.read_excel(
        'good-opt.xls',
        # 'good-opt-min.xls',
        'Каталог Молодежной одежды GOOD',
        usecols=opt_cols.keys(),
        names=opt_cols.values(),
        dtype=str,
        index_col=None,
        skiprows=8,
    )

    # пропускаем все с total_count = 0
    df_opt = df_opt[df_opt.total_count != '0']

    df_opt.fillna(0, inplace=True)  # Заменяем NaN на 0

    df_opt = df_opt[df_opt.product_code != 0]
    df_opt = df_opt[df_opt.product_name != 0]

    print('Основной каталог обработан за %s секунд.' % (time.time() - start_time))

    return df_opt


def init_info():
    start_time = time.time()
    print('Считываем вспомогательный каталог.')
    info_cols = {
        0: 'product_code',
        5: 'description_ru',
        7: 'gender',
        8: 'product_care',
        9: 'country',
    }
    df_info = pd.read_excel(
        'good-info.xls',
        'Молодежной одежды GOOD',
        usecols=info_cols.keys(),
        names=info_cols.values(),
        dtype=str,
        index_col=None,
        skiprows=8
    )

    df_info.fillna('', inplace=True)  # Заменяем NaN на 0
    print('Вспомогательный каталог обработан за %s секунд.' % (time.time() - start_time))

    return df_info


def init_imgs():
    start_time = time.time()
    print('Считываем каталог изображений.')
    imgs_cols = {
        0: 'product_code',
        1: 'images',
    }
    df_imgs = pd.read_csv(
        'imgsfile.csv',
        sep='\t',
        usecols=imgs_cols.keys(),
        names=imgs_cols.values(),
        dtype=str,
        index_col=None,
        # skiprows=8
    )

    # df_imgs.fillna('', inplace=True)  # Заменяем NaN на 0
    print('Вспомогательный каталог изображений обработан за %s секунд.' % (time.time() - start_time))

    return df_imgs


def init_vids():
    start_time = time.time()
    print('Считываем каталог видео.')
    vids_cols = {
        0: 'product_code',
        1: 'videos',
    }
    df_vids = pd.read_csv(
        'videosfile.csv',
        sep='\t',
        usecols=vids_cols.keys(),
        names=vids_cols.values(),
        dtype=str,
        index_col=None,
    )
    print('Вспомогательный каталог видео обработан за %s секунд.' % (time.time() - start_time))

    return df_vids


def pause():
    # os.system('pause')
    # return 0
    input("Press Enter to exit")


def get_int(value):
    return int(str(value).strip() or 0)


def get_str(value):
    return str(value).strip()


def get_bool(value):
    return 'Y' if value else 'N'


def get_product_name(value):
    list = value.split('\n')
    name = get_str(list[0])
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
        effects_temp = get_str(list[0])
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


def main():
    start_time = time.time()

    sizes = [
        'ns',
        '3xs',
        '2xs',
        'xs',
        's',
        'm',
        'l',
        'xl',
        '2xl',
        '3хl',
        '4хl',
        '5xl'
    ]

    def get_categories(a, b):
        m = ['%s///%s' % (x.strip(), y.strip()) for x in a for y in b]
        return '; '.join(m)

    def get_type(category):
        res = ''
        if len(category) > 1:
            pass
        else:
            res = category[0]
        return res

    # result_df = pd.concat([df_opt, df_info], axis=1, join="inner", on='code')
    temp_df = df_opt.merge(df_info, how='inner', on='product_code')
    temp_df = temp_df.merge(df_imgs, how='inner', on='product_code')
    temp_df = temp_df.merge(df_vids, how='inner', on='product_code')
    print('Каталоги обьединены.')

    temp_df['category'] = temp_df.apply(
        lambda row: get_categories(row.l1_category.split(';'), row.l2_category.split(';')), axis=1)
    temp_df['category_slug'] = temp_df.apply(
        lambda row: ' '.join([row.l1_category.split(';')[0], row.l2_category.split(';')[0]]), axis=1)
    # temp_df['type'] = temp_df.apply(
    #     lambda row: get_type(row.l1_category.split(';')), axis=1)
    temp_df.drop(['l1_category', 'l2_category'], axis=1, inplace=True)
    print('Обработаны категории.')

    res_df = pd.DataFrame()

    data = np.array([])

    for i, row in temp_df.iterrows():
        new_rows = np.array([])

        name, effects, stickers = get_product_name(row.product_name)

        variation_group_code = slugify('%s %s' % (row.category_slug, name))

        # quantity = get_int(row[size + '_size'])
        quantity = get_int(row.total_count)
        if quantity < 1:
            continue  # пропускаем товары с нулевым количеством
        code = get_str(row.product_code)
        # product_code = '%s-%s' % (code, size.upper())
        product_code = code
        brand = get_str(row.brand)
        slug_brand = slugify(brand)
        images = row.images
        videos = row.videos

        s = []
        stock = {}

        for size in sizes:
            size_count = get_int(row[size + '_size'])
            stock[size.upper()] = size_count

            # if size_count > 0:
            #     s.append('%s' % size.upper())

            s.append('%s' % size.upper())

            # if size_count > 0:
            #     s.append('%s%s'%(size.upper(),'///status=A'))
            # else:
            #     s.append('%s%s' % (size.upper(), '///status=D'))

        size_option = '(Gooood) Размер: SG[%s]' % ', '.join(s)

        s = []
        stock = {}
        for size in sizes:
            size_count = get_int(row[size + '_size'])
            stock[size.upper()] = size_count

            if size_count > 0:
                s.append('%s' % size.upper())

            # s.append('%s' % size.upper())

        size_feature = '%s' % '///'.join(s)

        e = []

        if effects['glow_in_the_dark']:
            e.append('Светится в темноте')
        if effects['glow_in_the_uv']:
            e.append('Светится в ультрафиолете')
        # effects_features = 'Эффекты: S[%s]' % ', '.join(e)
        effects_features = '%s' % '///'.join(e)

        popularity = (10000 - i) * 10000

        new_row = {
            'Product Code': product_code,
            'Product name': name,
            'Category': get_str(row.category),
            'Quantity': quantity,
            'Variation group code': variation_group_code,

            'Price': get_int(row.price),
            'List price': get_int(row.list_price),

            # 'Размер': size.upper(),
            # 'Размер': '',
            'Цвет': get_str(row.color),
            'Бренд': brand,
            'Артикул': code,
            'Уход за вещами': get_str(row.product_care),
            'Пол': get_str(row.gender),
            'Страна': get_str(row.country),
            'Options': size_option,
            # 'Features': s,
            'Стикеры': json.dumps(stickers),
            # 'Светится в темноте': get_bool(effects['glow_in_the_dark']),
            # 'Светится в ультрафмолете': get_bool(effects['glow_in_the_uv']),
            'Размер для фильтров': size_feature,
            'Эффекты': effects_features,
            'Раздел': get_str(row.product_type),
            'Количество в наличии': json.dumps(stock),
            'Состав': get_str(row.consists),
            'Description': get_str(row.description_ru),
            'Images': images,
            'Videos': videos,
            'Popularity': popularity
        }

        data = np.append(data, np.array(new_row))

    res_df = res_df.append(list(data), ignore_index=True)

    print(res_df)

    res_df.to_csv('csvfile.csv', encoding='utf-8', index=False, sep='\t')
    print("csvfile.csv сгенерирован за  %s секунл." % (time.time() - start_time))


def get_imgs():
    for i, row in df_opt.iterrows():
        print('%s\t%s' % (slugify(row.brand), get_str(row.product_code)))


def get_img_path():
    # path = Path('./images/products/good-fluro-power/14-1530/')
    # print(list(str(x) for x in path.glob('**/*')))

    print('Поиск изображений в ./images/products/{brand}/{sku}/')

    res_df = pd.DataFrame()
    data = np.array([])
    new_rows = np.array([])

    for i, row in df_opt.iterrows():
        # new_row = np.array([])
        # print('%s\t%s' % (slugify(row.brand), get_str(row.product_code)))
        path = Path('./images/products/%s/%s/' % (slugify(row.brand), get_str(row.product_code)))
        imgs = list(str(x) for x in natsort.natsorted(path.glob('**/*'), alg=natsort.PATH))
        # imgs = list(str(x) for x in sorted(path.glob('**/*'), key=natsort_key))
        print(imgs)
        images = '///'.join(imgs)

        new_row = {
            'Product Code': row.product_code,
            'Images': images
        }
        new_rows = np.append(new_rows, np.array(new_row))

    # new_rows = np.array()
    # data = np.concatenate((data, new_rows), axis=0)

    res_df = res_df.append(list(new_rows), ignore_index=True)

    res_df.to_csv('imgsfile.csv', encoding='utf-8', index=False, sep='\t')

    print('Изображения найдены и сохранены в imgsfile.csv за %s секунд.' % (time.time() - start_time))


def get_price():
    user_groups = {
        '- 11% от 110000р': {'row': 'price-11', 'group_id': 11},
        '- 3% от 30000р': {'row': 'price-3', 'group_id': 10},
        '- 7% от 70000р': {'row': 'price-7', 'group_id': 12},
        'Мелкий опт от 10шт.': {'row': 'small_opt_price', 'group_id': 8},
        'Опт. от 15000р': {'row': 'opt_price', 'group_id': 9},
        '-10% от оптовой цены': {'row': 'price-10', 'group_id': 23},
        '-15% от оптовой цены': {'row': 'price-15', 'group_id': 24},
        '-20% от оптовой цены': {'row': 'price-20', 'group_id': 25},
        '-22% от оптовой цены': {'row': 'price-22', 'group_id': 26},
        '-25% от оптовой цены': {'row': 'price-25', 'group_id': 27},
    }

    res_df = pd.DataFrame()

    data = np.array([])

    for i, row in df_opt.iterrows():

        quantity = get_int(row.total_count)
        if quantity < 1:
            continue  # пропускаем товары с нулевым количеством
        code = get_str(row.product_code)
        product_code = code

        for key, value in user_groups.items():
            new_row = {
                'Product code': product_code,
                'Language': 'ru',
                'Price': get_int(row[value['row']]),
                # 'Percentage discount':value,
                'Lower limit': 1,
                'User group': key,
                # 'Название группы': key
                # 'Product name': name,
                # 'Category': get_str(row.category),
                # 'Quantity': quantity,
                # 'Variation group code': variation_group_code,
            }

            data = np.append(data, np.array(new_row))

    res_df = res_df.append(list(data), ignore_index=True)

    print(res_df)

    res_df.to_csv('opt_price.csv', encoding='utf-8', index=False, sep='\t')


def get_video_path():
    # path = Path('./images/products/good-fluro-power/14-1530/')
    # print(list(str(x) for x in path.glob('**/*')))

    print('Поиск видео в ./video/products/{brand}/{sku}/')

    res_df = pd.DataFrame()
    data = np.array([])
    new_rows = np.array([])

    for i, row in df_opt.iterrows():
        # new_row = np.array([])
        # print('%s\t%s' % (slugify(row.brand), get_str(row.product_code)))
        path = Path('./video/products/%s/%s/' % (slugify(row.brand), get_str(row.product_code)))
        vids = list(str(x) for x in natsort.natsorted(path.glob('**/*'), alg=natsort.PATH))
        # imgs = list(str(x) for x in sorted(path.glob('**/*'), key=natsort_key))
        print(vids)
        # videos = '///'.join(vids)
        videos = json.dumps(vids)

        new_row = {
            'Product Code': row.product_code,
            'Videos': videos
        }
        new_rows = np.append(new_rows, np.array(new_row))

    # new_rows = np.array()
    # data = np.concatenate((data, new_rows), axis=0)

    res_df = res_df.append(list(new_rows), ignore_index=True)

    res_df.to_csv('videosfile.csv', encoding='utf-8', index=False, sep='\t')

    print('Видео найдены и сохранены в videosfile.csv за %s секунд.' % (time.time() - start_time))


start_time = time.time()
print('Начали работу.')

# df_opt = init_main()
# df_info = init_info()
# # get_imgs()
# get_img_path()
# get_video_path()
#
# df_imgs = init_imgs()
# df_vids = init_vids()
# main()
#
# get_price()

my_price_generator = PriceGenerator()
my_price_generator.get_price()


print('Общее время работы:  %s секунд.' % (time.time() - start_time))

# print('Hello world')
# pause()
