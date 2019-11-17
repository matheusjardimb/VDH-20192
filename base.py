import json
import random

HOURS_DAY = 24
HOUR_MIN = 60
DAY_MIN = HOUR_MIN * HOURS_DAY

DOM = 0
SEG = 1
TER = 2
QUA = 3
QUI = 4
SEX = 5
SAB = 6


def get_weekday_idx(week_day):
    if week_day == 'DOMINGO':
        return 0
    if week_day == 'SEGUNDA-FEIRA':
        return 1
    if week_day == 'TERCA-FEIRA':
        return 2
    if week_day == 'QUARTA-FEIRA':
        return 3
    if week_day == 'QUINTA-FEIRA':
        return 4
    if week_day == 'SEXTA-FEIRA':
        return 5
    if week_day == 'SABADO':
        return 6


def get_idx(week_day, hour, minute):
    return minute + (hour * HOUR_MIN) + (week_day * DAY_MIN)


def find_indices(lst, condition):
    return [(i, elem) for i, elem in enumerate(lst) if condition(elem)]


def get_rgb():
    r = str(random.randint(1, 254))
    g = str(random.randint(1, 254))
    b = str(random.randint(1, 254))
    return ', '.join([b, g, r])


def get_series_item(row_data, year):
    return {
        'name': year,
        'color': 'rgba(' + get_rgb() + ', .5)',
        'data': row_data,
        'visible': False,
        'sizeByAbsoluteValue': True,
    }


def get_hora_idx(columns):
    try:
        return columns.index('HORA')
    except:
        return columns.index('DATA_HORA')


def generate_output_file(add_general_data, files, general_data, group_by_minutes, only_fatal, series, date_conds,
                         ignore_weekday):
    if add_general_data:
        series.append(get_series_item(general_data, 'Geral'))
    output_name = \
        '__years=' + ','.join([x[23:25] for x in files.keys()]) + \
        '__add_general_data=' + str(add_general_data) + \
        '__group_by_minutes=' + str(group_by_minutes) + \
        '__only_fatal=' + str(only_fatal) + \
        '__ignore_weekday=' + str(ignore_weekday) + \
        '__date_conds=' + str(len(date_conds)) + \
        '.json'
    file_object = open('res/' + output_name, 'w')
    json.dump({'series': series}, file_object)


def get_year(file_name):
    return file_name.split('/')[2]


vehicles = {
    'AUTO': [],
    'TAXI': [],
    'LOTACAO': [],
    'ONIBUS_URB': [],
    'ONIBUS_MET': [],
    'ONIBUS_INT': [],
    'CAMINHAO': [],
    'MOTO': [],
    'CARROCA': [],
    'BICICLETA': [],
    'OUTRO': [],
}
