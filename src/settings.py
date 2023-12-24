from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

SIZES = [
    'ns',
    '3xs',
    '2xs',
    'xs',
    's',
    'm',
    'l',
    'xl',
    '2xl',
    '3xl',
    '4xl',
    '5xl'
]

SIZES_K = [
    # 'ns',
    '98',
    '104',
    '110',
    '116',
    '122',
    '128',
    '134',
    '140',
    '146',
    '152',
    '158',
]

USER_GROUPS = {
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

xls_files_list = {
    'good_opt': {
        # 'file': BASE_DIR / 'in' / 'good-opt.xls',
        'file': BASE_DIR.parent / 'price' / 'good-opt.xls',
        'sheet': 'Каталог Молодежной одежды GOOD',
        'cols': {
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
            33: '3xl_size',
            34: '4xl_size',
            35: '5xl_size',
        },
        'skip_rows': 8,
        'skip_empty_fields': ['product_code', ],
        'skip_brands': [
            'АРТимперия',
            'Fandesire',
            # 'GOOD FLURO POWER',
            # 'TON'
        ],
    },
    'good_info': {
        # 'file': BASE_DIR / 'in' / 'good-info.xls',
        'file': BASE_DIR.parent / 'price' / 'good-info.xls',
        'sheet': 'Молодежной одежды GOOD',
        'cols': {
            0: 'product_code',
            5: 'description_ru',
            7: 'gender',
            8: 'product_care',
            9: 'country',
            10: 'add_date',
            11: 'popularity'
        },
        'skip_rows': 8,
        'skip_empty_fields': ['product_code', ],
        'skip_brands': [],
    },
    'images': {
        'file': BASE_DIR / 'out' / 'images_files.csv',
        'cols': {
            0: 'product_code',
            1: 'images'
        },
        'skip_rows': 0,
        'skip_empty_fields': [],
        'skip_brands': [],
    },
    'video': {
        'file': BASE_DIR / 'out' / 'video_files.csv',
        'cols': {
            0: 'product_code',
            1: 'video'
        },
        'skip_rows': 0,
        'skip_empty_fields': [],
        'skip_brands': [],
    }
}