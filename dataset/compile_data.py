# coding=utf-8
import csv
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

data_by_year = {
    '2016/acidentes-2016.csv': [
        'ID', 'LONGITUDE', 'LATITUDE', 'LOG1', 'LOG2', 'PREDIAL1', 'LOCAL', 'TIPO_ACID', 'LOCAL_VIA', 'QUEDA_ARR',
        'DATA', 'DATA_HORA', 'DIA_SEM', 'HORA', 'FERIDOS', 'FERIDOS_GR', 'MORTES', 'MORTE_POST', 'FATAIS', 'AUTO',
        'TAXI', 'LOTACAO', 'ONIBUS_URB', 'ONIBUS_MET', 'ONIBUS_INT', 'CAMINHAO', 'MOTO', 'CARROCA', 'BICICLETA',
        'OUTRO', 'TEMPO', 'NOITE_DIA', 'FONTE', 'BOLETIM', 'REGIAO', 'DIA', 'MES', 'ANO', 'FX_HORA', 'CONT_ACID',
        'CONT_VIT', 'UPS', 'CONSORCIO', 'CORREDOR',
    ],
    '2015/acidentes-2015.csv': [
        'ID', 'LOG1', 'LOG2', 'PREDIAL1', 'LOCAL', 'TIPO_ACID', 'LOCAL_VIA', 'QUEDA_ARR', 'DATA_HORA', 'DATA',
        'DIA_SEM', 'HORA', 'FERIDOS', 'FERIDOS_GR', 'MORTES', 'MORTE_POST', 'FATAIS', 'AUTO', 'TAXI', 'LOTACAO',
        'ONIBUS_URB', 'ONIBUS_MET', 'ONIBUS_INT', 'CAMINHAO', 'MOTO', 'CARROCA', 'BICICLETA', 'OUTRO', 'TEMPO',
        'NOITE_DIA', 'FONTE', 'BOLETIM', 'REGIAO', 'DIA', 'MES', 'ANO', 'FX_HORA', 'CONT_ACID', 'CONT_VIT', 'UPS',
        'CONSORCIO', 'CORREDOR', 'LONGITUDE', 'LATITUDE',
    ],
}


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


def update_rows(row_data, x, y):
    res = find_indices(row_data, lambda e: e['x'] == x and e['y'] == y)
    if len(res):
        i, el = res[0]
        row_data[i]['z'] = el['z'] + 1
        row_data[i]['count'] = el['count'] + 1
    else:
        row_data.append({'x': x, 'y': y, 'z': 1, 'count': 1})


def generate_json(data):
    series = []
    general_data = []

    for file_name, columns in data.items():
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
        year = file_name.split('/')[0]
        with open(file_name) as csv_file:
            HORA_idx = columns.index('HORA')
            DIA_SEM_idx = columns.index('DIA_SEM')
            FATAIS_idx = columns.index('FATAIS')

            row_data = []
            reader = csv.reader(csv_file, delimiter=';')
            next(reader, None)  # skip the headers

            for row in reader:
                time = row[HORA_idx]
                if not time:
                    continue  # Ignore rows without time

                hour, minute = time.split(':')
                x = get_idx(get_weekday_idx(row[DIA_SEM_idx]), int(hour), int(minute))

                y = int(row[FATAIS_idx])

                # if VEHICLE_idx:
                #     has_v = row[VEHICLE_idx]
                #     if not has_v or has_v == '0':
                #         continue

                # for v in vehicles:
                #     v_idx = columns.index(v)

                update_rows(row_data, x, y)
                update_rows(general_data, x, y)

            series.append(get_series_item(row_data, year))

    series.append(get_series_item(general_data, 'Geral'))

    file_object = open('results.json', 'w')
    json.dump({'series': series}, file_object)


generate_json(data_by_year)
