#!/usr/bin/env python3

import pandas
import pandas as pd
import numpy as np
from slugify import slugify
from pathlib import Path

import time
# from natsort import natsort_key
# from natsort import natsorted
import natsort

import json


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
        18: 'total_count',
        19: 'ns_size',
        20: '3xs_size',
        21: '2xs_size',
        22: 'xs_size',
        23: 's_size',
        24: 'm_size',
        25: 'l_size',
        26: 'xl_size',
        27: '2xl_size',
        28: '3хl_size',
        29: '4хl_size',
        30: '5xl_size',
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

        # data = np.concatenate((data, new_rows), axis=0)

        #
        #     quantity = get_int(row[size + '_size'])
        #     if quantity < 1:
        #         continue    # пропускаем товары с нулевым количеством
        #     code = get_str(row.product_code)
        #     product_code = '%s-%s' % (code, size.upper())
        #     brand = get_str(row.brand)
        #     slug_brand = slugify(brand)
        #     images = row.images
        #
        #
        #     new_row = {
        #         'Product Code': product_code,
        #         'Product name': name,
        #         'Category': get_str(row.category),
        #         'Quantity': quantity,
        #         'Variation group code': variation_group_code,
        #
        #         'Price' : get_int(row.price),
        #         'List price' : get_int(row.list_price),
        #
        #         'Размер': size.upper(),
        #         'Цвет': get_str(row.color),
        #         'Бренд': brand,
        #         'Артикул': code,
        #         'Уход за вещами': get_str(row.product_care),
        #         'Пол': get_str(row.gender),
        #         'Страна':get_str(row.country),
        #
        #         'Состав': get_str(row.consists),
        #         'Description': get_str(row.description_ru),
        #         'Images': images
        #     }
        #
        #     new_rows = np.append(new_rows, np.array(new_row))
        #
        # data = np.concatenate((data, new_rows), axis=0)
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
        videos = '///'.join(vids)

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

df_opt = init_main()
df_info = init_info()
# get_imgs()
# get_img_path()
# get_video_path()

df_imgs = init_imgs()
df_vids = init_vids()
main()

# my_path = Path('.')
# print(list(my_path.rglob('./gd/*b.jpg')))

print('Общее время работы:  %s секунд.' % (time.time() - start_time))

# print('Hello world')
# pause()
