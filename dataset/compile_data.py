# coding=utf-8
import csv
import json

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
        'DATA', 'DATA_HORA', 'DIA_SEM', 'HORA', 'FERIDOS', 'FERIDOS_GR', 'MORTES', 'MORTE_POST', 'FATAIS',

        'AUTO', 'TAXI', 'LOTACAO', 'ONIBUS_URB', 'ONIBUS_MET', 'ONIBUS_INT', 'CAMINHAO', 'MOTO', 'CARROCA', 'BICICLETA',
        'OUTRO',  # Tipos de veículos envolvidos

        'TEMPO', 'NOITE_DIA', 'FONTE', 'BOLETIM', 'REGIAO', 'DIA', 'MES', 'ANO', 'FX_HORA', 'CONT_ACID',
        'CONT_VIT', 'UPS', 'CONSORCIO', 'CORREDOR',
    ]
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


def generate_json(data):
    series = []

    for file_name, columns in data.items():
        with open(file_name) as csv_file:
            HORA_idx = columns.index('HORA')
            DIA_SEM_idx = columns.index('DIA_SEM')
            FATAIS_idx = columns.index('FATAIS')

            row_data = []
            reader = csv.reader(csv_file, delimiter=';')
            next(reader, None)  # skip the headers
            for row in reader:
                week_day = get_weekday_idx(row[DIA_SEM_idx])
                time = row[HORA_idx]
                if not time:
                    continue  # Ignore rows without time

                hour, minute = time.split(':')
                x = get_idx(week_day, int(hour), int(minute))
                y = int(row[FATAIS_idx])

                res = find_indices(row_data, lambda e: e['x'] == x and e['y'] == y)
                if len(res):
                    i, el = res[0]
                    row_data[i]['z'] = el['z'] + 1
                else:
                    row_data.append({'x': x, 'y': y, 'z': 1})

            series.append({
                'name': 'Geral',
                'color': 'rgba(23, 83, 83, .5)',
                'data': row_data
            })

            file_object = open(file_name + '.json', 'w')
            json.dump({'series': series}, file_object)


generate_json(data_by_year)
