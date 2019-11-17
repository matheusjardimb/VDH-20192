import csv

from base import *


def update_rows(row_data, x, y):
    res = find_indices(row_data, lambda e: e['x'] == x and e['y'] == y)
    if len(res):
        i, el = res[0]
        row_data[i]['z'] = el['z'] + 1
        row_data[i]['count'] = el['count'] + 1
    else:
        row_data.append({'x': x, 'y': y, 'z': 1, 'count': 1})


def check_date_condition(DIA_idx, MES_idx, ANO_idx, date_conds, row):
    if date_conds:
        for cond in date_conds:
            day_check = (cond['day'] and cond['day'] == int(row[DIA_idx])) or not cond['day']
            month_check = (cond['month'] and cond['month'] == int(row[MES_idx])) or not cond['month']
            year_check = (cond['year'] and cond['year'] == int(row[ANO_idx])) or not cond['year']
            if day_check and month_check and year_check:
                return True
    return False


def generate_json(files, add_general_data, group_by_minutes, only_fatal, date_conds, ignore_weekday):
    series = []
    general_data = []

    total_fatal = 0
    for file_name, columns in files.items():
        invalid_row = 0
        year_fatal = 0

        year = get_year(file_name)

        HORA_idx = get_hora_idx(columns)
        DIA_SEM_idx = columns.index('DIA_SEM')
        FATAIS_idx = columns.index('FATAIS')
        DIA_idx = columns.index('DIA')
        MES_idx = columns.index('MES')
        ANO_idx = columns.index('ANO')

        row_data = []

        with open(file_name) as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            next(reader, None)  # skip the headers

            for row in reader:
                try:
                    time = row[HORA_idx]
                    if not time:
                        invalid_row += 1
                        continue  # Ignore rows without time

                    y = int(row[FATAIS_idx])
                    if only_fatal and not y:
                        continue
                    total_fatal += y
                    year_fatal += y

                    if not check_date_condition(DIA_idx, MES_idx, ANO_idx, date_conds, row):
                        continue

                    if ' ' in time:
                        time = time.split(' ')[1]  # some csv have '20130101 02:10', so we're removing date
                    hour, minute = time.split(':')
                    minutes = int(minute)
                    if group_by_minutes:
                        minutes = minutes // group_by_minutes * group_by_minutes
                    if ignore_weekday:
                        weekday_idx = 7
                    else:
                        weekday_idx = get_weekday_idx(row[DIA_SEM_idx])
                    x = get_idx(weekday_idx, int(hour), minutes)

                    update_rows(row_data, x, y)
                    update_rows(general_data, x, y)
                except Exception as e:  # noqa
                    invalid_row += 1

            series.append(get_series_item(row_data, year))
            print('[%s-INFO] Valid rows: %s' % (year, len(row_data)))
            print('[%s-INFO] Invalid rows: %s' % (year, invalid_row))

        print('[%s-INFO] year_fatal: %s' % (year, year_fatal))
        print('')

    print('[INFO] total_fatal: %s' % total_fatal)

    generate_output_file(
        add_general_data, files, general_data, group_by_minutes, only_fatal, series, date_conds, ignore_weekday
    )


data = {
    '../dataset/acidentes-2016.csv': [
        'ID', 'LONGITUDE', 'LATITUDE', 'LOG1', 'LOG2', 'PREDIAL1', 'LOCAL', 'TIPO_ACID', 'LOCAL_VIA', 'QUEDA_ARR',
        'DATA', 'DATA_HORA', 'DIA_SEM', 'HORA', 'FERIDOS', 'FERIDOS_GR', 'MORTES', 'MORTE_POST', 'FATAIS', 'AUTO',
        'TAXI', 'LOTACAO', 'ONIBUS_URB', 'ONIBUS_MET', 'ONIBUS_INT', 'CAMINHAO', 'MOTO', 'CARROCA', 'BICICLETA',
        'OUTRO', 'TEMPO', 'NOITE_DIA', 'FONTE', 'BOLETIM', 'REGIAO', 'DIA', 'MES', 'ANO', 'FX_HORA', 'CONT_ACID',
        'CONT_VIT', 'UPS', 'CONSORCIO', 'CORREDOR',
    ],
    '../dataset/acidentes-2015.csv': [
        'ID', 'LOG1', 'LOG2', 'PREDIAL1', 'LOCAL', 'TIPO_ACID', 'LOCAL_VIA', 'QUEDA_ARR', 'DATA_HORA', 'DATA',
        'DIA_SEM', 'HORA', 'FERIDOS', 'FERIDOS_GR', 'MORTES', 'MORTE_POST', 'FATAIS', 'AUTO', 'TAXI', 'LOTACAO',
        'ONIBUS_URB', 'ONIBUS_MET', 'ONIBUS_INT', 'CAMINHAO', 'MOTO', 'CARROCA', 'BICICLETA', 'OUTRO', 'TEMPO',
        'NOITE_DIA', 'FONTE', 'BOLETIM', 'REGIAO', 'DIA', 'MES', 'ANO', 'FX_HORA', 'CONT_ACID', 'CONT_VIT', 'UPS',
        'CONSORCIO', 'CORREDOR', 'LONGITUDE', 'LATITUDE',
    ],
    '../dataset/acidentes-2014.csv': [
        'ID', 'LOCAL_VIA', 'LOG1', 'LOG2', 'PREDIAL1', 'LOCAL', 'TIPO_ACID', 'QUEDA_ARR', 'DATA_HORA', 'DATA',
        'DIA_SEM', 'HORA', 'FERIDOS', 'FERIDOS_GR', 'MORTES', 'MORTE_POST', 'FATAIS', 'AUTO', 'TAXI', 'LOTACAO',
        'ONIBUS_URB', 'ONIBUS_MET', 'ONIBUS_INT', 'CAMINHAO', 'MOTO', 'CARROCA', 'BICICLETA', 'OUTRO', 'TEMPO',
        'NOITE_DIA', 'FONTE', 'BOLETIM', 'REGIAO', 'DIA', 'MES', 'ANO', 'FX_HORA', 'CONT_ACID', 'CONT_VIT', 'UPS',
        'CONSORCIO', 'CORREDOR', 'LONGITUDE', 'LATITUDE',
    ],
    '../dataset/acidentes-2013.csv': [
        'ID', 'LOG1', 'LOG2', 'PREDIAL1', 'LOCAL', 'TIPO_ACID', 'LOCAL_VIA', 'QUEDA_ARR', 'DATA_HORA', 'DIA_SEM',
        'FERIDOS', 'FERIDOS_GR', 'MORTES', 'MORTE_POST', 'FATAIS', 'AUTO', 'TAXI', 'LOTACAO', 'ONIBUS_URB',
        'ONIBUS_MET', 'ONIBUS_INT', 'CAMINHAO', 'MOTO', 'CARROCA', 'BICICLETA', 'OUTRO', 'TEMPO', 'NOITE_DIA',
        'FONTE', 'BOLETIM', 'REGIAO', 'DIA', 'MES', 'ANO', 'FX_HORA', 'CONT_ACID', 'CONT_VIT', 'UPS', 'CONSORCIO',
        'CORREDOR', 'LONGITUDE', 'LATITUDE',
    ],
    '../dataset/acidentes-2012.csv': [
        'ID', 'LOG1', 'LOG2', 'PREDIAL1', 'LOCAL', 'TIPO_ACID', 'LOCAL_VIA', 'DATA_HORA', 'DIA_SEM', 'FERIDOS',
        'MORTES', 'MORTE_POST', 'FATAIS', 'AUTO', 'TAXI', 'LOTACAO', 'ONIBUS_URB', 'ONIBUS_INT', 'CAMINHAO', 'MOTO',
        'CARROCA', 'BICICLETA', 'OUTRO', 'TEMPO', 'NOITE_DIA', 'FONTE', 'BOLETIM', 'REGIAO', 'DIA', 'MES', 'ANO',
        'FX_HORA', 'CONT_ACID', 'CONT_VIT', 'UPS', 'LATITUDE', 'LONGITUDE',
    ],
    '../dataset/acidentes-2011.csv': [
        'ID', 'LOG1', 'LOG2', 'PREDIAL1', 'LOCAL', 'TIPO_ACID', 'LOCAL_VIA', 'DATA_HORA', 'DIA_SEM', 'FERIDOS',
        'MORTES', 'MORTE_POST', 'FATAIS', 'AUTO', 'TAXI', 'LOTACAO', 'ONIBUS_URB', 'ONIBUS_INT', 'CAMINHAO', 'MOTO',
        'CARROCA', 'BICICLETA', 'OUTRO', 'TEMPO', 'NOITE_DIA', 'FONTE', 'BOLETIM', 'REGIAO', 'DIA', 'MES', 'ANO',
        'FX_HORA', 'CONT_ACID', 'CONT_VIT', 'UPS', 'LATITUDE', 'LONGITUDE',
    ],
    '../dataset/acidentes-2010.csv': [
        'ID', 'LOG1', 'LOG2', 'PREDIAL1', 'LOCAL', 'TIPO_ACID', 'LOCAL_VIA', 'DATA_HORA', 'DIA_SEM', 'FERIDOS',
        'MORTES', 'MORTE_POST', 'FATAIS', 'AUTO', 'TAXI', 'LOTACAO', 'ONIBUS_URB', 'ONIBUS_INT', 'CAMINHAO', 'MOTO',
        'CARROCA', 'BICICLETA', 'OUTRO', 'TEMPO', 'NOITE_DIA', 'FONTE', 'BOLETIM', 'REGIAO', 'DIA', 'MES', 'ANO',
        'FX_HORA', 'CONT_ACID', 'CONT_VIT', 'UPS', 'LATITUDE', 'LONGITUDE',
    ],
}

generate_json(
    files=data,  # which files to consider
    add_general_data=True,  # whether should generate 'general' series
    group_by_minutes=60,  # group events by minutes; None disables it
    only_fatal=False,  # ignore non-fatal accidents
    ignore_weekday=False,  # threats every data as the same weekday
    date_conds=[
        # # Qualquer dia
        {'day': None, 'month': None, 'year': None},

        # # Ano Novo
        # {'day': 1, 'month': 1, 'year': None},
        #
        # # Dia dos Namorados
        # {'day': 12, 'month': 6, 'year': None},
        #
        # # Nossa Senhora dos Navegantes
        # {'day': 2, 'month': 2, 'year': None},
        #
        # # Independencia do Brasil
        # {'day': 7, 'month': 9, 'year': None},
        #
        # # Aniversario de Porto Alegre
        # {'day': 26, 'month': 3, 'year': None},
        #
        # # Revolucao Farroupilha
        # {'day': 20, 'month': 9, 'year': None},
        #
        # # Nossa Senhora Aparecida
        # {'day': 12, 'month': 10, 'year': None},
        #
        # # Dia do Trabalhador
        # {'day': 1, 'month': 5, 'year': None},
        #
        # # Finados
        # {'day': 2, 'month': 11, 'year': None},
        #
        # # Natal
        # {'day': 25, 'month': 12, 'year': None},
        #
        # # Proclamacao da Republica
        # {'day': 15, 'month': 11, 'year': None},
        #
        # # Dia dos pais
        # {'day': 8, 'month': 8, 'year': 2010},
        # {'day': 14, 'month': 8, 'year': 2011},
        # {'day': 12, 'month': 8, 'year': 2012},
        # {'day': 11, 'month': 8, 'year': 2013},
        # {'day': 10, 'month': 8, 'year': 2014},
        # {'day': 9, 'month': 8, 'year': 2015},
        # {'day': 14, 'month': 8, 'year': 2016},
        #
        # # Carnaval
        # {'day': 16, 'month': 2, 'year': 2010},
        # {'day': 8, 'month': 3, 'year': 2011},
        # {'day': 21, 'month': 2, 'year': 2012},
        # {'day': 12, 'month': 2, 'year': 2013},
        # {'day': 4, 'month': 3, 'year': 2014},
        # {'day': 17, 'month': 2, 'year': 2015},
        # {'day': 9, 'month': 2, 'year': 2016},
        #
        # # Paixao de Cristo/Pascoa
        # {'day': 4, 'month': 4, 'year': 2010},
        # {'day': 24, 'month': 4, 'year': 2011},
        # {'day': 8, 'month': 4, 'year': 2012},
        # {'day': 31, 'month': 3, 'year': 2013},
        # {'day': 20, 'month': 4, 'year': 2014},
        # {'day': 5, 'month': 4, 'year': 2015},
        # {'day': 27, 'month': 3, 'year': 2016},
        #
        # # Dia das maes
        # {'day': 9, 'month': 5, 'year': 2010},
        # {'day': 8, 'month': 5, 'year': 2011},
        # {'day': 13, 'month': 5, 'year': 2012},
        # {'day': 12, 'month': 5, 'year': 2013},
        # {'day': 11, 'month': 5, 'year': 2014},
        # {'day': 10, 'month': 5, 'year': 2015},
        # {'day': 8, 'month': 5, 'year': 2016},
        #
        # # Corpus Christi
        # {'day': 3, 'month': 6, 'year': 2010},
        # {'day': 23, 'month': 6, 'year': 2011},
        # {'day': 7, 'month': 6, 'year': 2012},
        # {'day': 30, 'month': 5, 'year': 2013},
        # {'day': 19, 'month': 6, 'year': 2014},
        # {'day': 4, 'month': 6, 'year': 2015},
        # {'day': 26, 'month': 5, 'year': 2016},
    ],
)
