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
        '__data=' + ','.join([x.split('/')[2][2:4] for x in files.keys()]) + \
        '__add_general_data=' + str(add_general_data) + \
        '__group_by_minutes=' + str(group_by_minutes) + \
        '__only_fatal=' + str(only_fatal) + \
        '__date_conds=' + str(len(date_conds)) + \
        '__ignore_weekday=' + str(ignore_weekday) + \
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

data = {
    '../dataset/2016/acidentes-2016.csv': [
        'ID', 'LONGITUDE', 'LATITUDE', 'LOG1', 'LOG2', 'PREDIAL1', 'LOCAL', 'TIPO_ACID', 'LOCAL_VIA', 'QUEDA_ARR',
        'DATA', 'DATA_HORA', 'DIA_SEM', 'HORA', 'FERIDOS', 'FERIDOS_GR', 'MORTES', 'MORTE_POST', 'FATAIS', 'AUTO',
        'TAXI', 'LOTACAO', 'ONIBUS_URB', 'ONIBUS_MET', 'ONIBUS_INT', 'CAMINHAO', 'MOTO', 'CARROCA', 'BICICLETA',
        'OUTRO', 'TEMPO', 'NOITE_DIA', 'FONTE', 'BOLETIM', 'REGIAO', 'DIA', 'MES', 'ANO', 'FX_HORA', 'CONT_ACID',
        'CONT_VIT', 'UPS', 'CONSORCIO', 'CORREDOR',
    ],
    '../dataset/2015/acidentes-2015.csv': [
        'ID', 'LOG1', 'LOG2', 'PREDIAL1', 'LOCAL', 'TIPO_ACID', 'LOCAL_VIA', 'QUEDA_ARR', 'DATA_HORA', 'DATA',
        'DIA_SEM', 'HORA', 'FERIDOS', 'FERIDOS_GR', 'MORTES', 'MORTE_POST', 'FATAIS', 'AUTO', 'TAXI', 'LOTACAO',
        'ONIBUS_URB', 'ONIBUS_MET', 'ONIBUS_INT', 'CAMINHAO', 'MOTO', 'CARROCA', 'BICICLETA', 'OUTRO', 'TEMPO',
        'NOITE_DIA', 'FONTE', 'BOLETIM', 'REGIAO', 'DIA', 'MES', 'ANO', 'FX_HORA', 'CONT_ACID', 'CONT_VIT', 'UPS',
        'CONSORCIO', 'CORREDOR', 'LONGITUDE', 'LATITUDE',
    ],
    '../dataset/2014/acidentes-2014.csv': [
        'ID', 'LOCAL_VIA', 'LOG1', 'LOG2', 'PREDIAL1', 'LOCAL', 'TIPO_ACID', 'QUEDA_ARR', 'DATA_HORA', 'DATA',
        'DIA_SEM', 'HORA', 'FERIDOS', 'FERIDOS_GR', 'MORTES', 'MORTE_POST', 'FATAIS', 'AUTO', 'TAXI', 'LOTACAO',
        'ONIBUS_URB', 'ONIBUS_MET', 'ONIBUS_INT', 'CAMINHAO', 'MOTO', 'CARROCA', 'BICICLETA', 'OUTRO', 'TEMPO',
        'NOITE_DIA', 'FONTE', 'BOLETIM', 'REGIAO', 'DIA', 'MES', 'ANO', 'FX_HORA', 'CONT_ACID', 'CONT_VIT', 'UPS',
        'CONSORCIO', 'CORREDOR', 'LONGITUDE', 'LATITUDE',
    ],
    '../dataset/2013/acidentes-2013.csv': [
        'ID', 'LOG1', 'LOG2', 'PREDIAL1', 'LOCAL', 'TIPO_ACID', 'LOCAL_VIA', 'QUEDA_ARR', 'DATA_HORA', 'DIA_SEM',
        'FERIDOS', 'FERIDOS_GR', 'MORTES', 'MORTE_POST', 'FATAIS', 'AUTO', 'TAXI', 'LOTACAO', 'ONIBUS_URB',
        'ONIBUS_MET', 'ONIBUS_INT', 'CAMINHAO', 'MOTO', 'CARROCA', 'BICICLETA', 'OUTRO', 'TEMPO', 'NOITE_DIA',
        'FONTE', 'BOLETIM', 'REGIAO', 'DIA', 'MES', 'ANO', 'FX_HORA', 'CONT_ACID', 'CONT_VIT', 'UPS', 'CONSORCIO',
        'CORREDOR', 'LONGITUDE', 'LATITUDE',
    ],
    '../dataset/2012/acidentes-2012.csv': [
        'ID', 'LOG1', 'LOG2', 'PREDIAL1', 'LOCAL', 'TIPO_ACID', 'LOCAL_VIA', 'DATA_HORA', 'DIA_SEM', 'FERIDOS',
        'MORTES', 'MORTE_POST', 'FATAIS', 'AUTO', 'TAXI', 'LOTACAO', 'ONIBUS_URB', 'ONIBUS_INT', 'CAMINHAO', 'MOTO',
        'CARROCA', 'BICICLETA', 'OUTRO', 'TEMPO', 'NOITE_DIA', 'FONTE', 'BOLETIM', 'REGIAO', 'DIA', 'MES', 'ANO',
        'FX_HORA', 'CONT_ACID', 'CONT_VIT', 'UPS', 'LATITUDE', 'LONGITUDE',
    ],
    '../dataset/2011/acidentes-2011.csv': [
        'ID', 'LOG1', 'LOG2', 'PREDIAL1', 'LOCAL', 'TIPO_ACID', 'LOCAL_VIA', 'DATA_HORA', 'DIA_SEM', 'FERIDOS',
        'MORTES', 'MORTE_POST', 'FATAIS', 'AUTO', 'TAXI', 'LOTACAO', 'ONIBUS_URB', 'ONIBUS_INT', 'CAMINHAO', 'MOTO',
        'CARROCA', 'BICICLETA', 'OUTRO', 'TEMPO', 'NOITE_DIA', 'FONTE', 'BOLETIM', 'REGIAO', 'DIA', 'MES', 'ANO',
        'FX_HORA', 'CONT_ACID', 'CONT_VIT', 'UPS', 'LATITUDE', 'LONGITUDE',
    ],
    '../dataset/2010/acidentes-2010.csv': [
        'ID', 'LOG1', 'LOG2', 'PREDIAL1', 'LOCAL', 'TIPO_ACID', 'LOCAL_VIA', 'DATA_HORA', 'DIA_SEM', 'FERIDOS',
        'MORTES', 'MORTE_POST', 'FATAIS', 'AUTO', 'TAXI', 'LOTACAO', 'ONIBUS_URB', 'ONIBUS_INT', 'CAMINHAO', 'MOTO',
        'CARROCA', 'BICICLETA', 'OUTRO', 'TEMPO', 'NOITE_DIA', 'FONTE', 'BOLETIM', 'REGIAO', 'DIA', 'MES', 'ANO',
        'FX_HORA', 'CONT_ACID', 'CONT_VIT', 'UPS', 'LATITUDE', 'LONGITUDE',
    ],
}
