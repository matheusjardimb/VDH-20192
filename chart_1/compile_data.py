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


def check_date_condition(DIA_idx, MES_idx, date_conds, row):
    if date_conds:
        for cond in date_conds:
            day_check = (cond['day'] and cond['day'] == int(row[DIA_idx])) or not cond['day']
            month_check = (cond['month'] and cond['month'] == int(row[MES_idx])) or not cond['month']
            if day_check and month_check:
                return True
    return False


def generate_json(files, add_general_data, group_by_minutes, only_fatal, date_conds, ignore_weekday):
    series = []
    general_data = []

    for file_name, columns in files.items():
        invalid_row = 0

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

                    if not check_date_condition(DIA_idx, MES_idx, date_conds, row):
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

                    # if VEHICLE_idx:
                    #     has_v = row[VEHICLE_idx]
                    #     if not has_v or has_v == '0':
                    #         continue

                    # for v in vehicles:
                    #     v_idx = columns.index(v)

                    update_rows(row_data, x, y)
                    update_rows(general_data, x, y)
                except Exception as e:  # noqa
                    invalid_row += 1
                    # print('[%s-ERROR]Ignoring row : %s' % (year, row))

            series.append(get_series_item(row_data, year))
            print('[%s-INFO]Valid rows: %s' % (year, len(row_data)))
            print('[%s-INFO]Invalid rows: %s' % (year, invalid_row))

    generate_output_file(
        add_general_data, files, general_data, group_by_minutes, only_fatal, series, date_conds, ignore_weekday
    )


generate_json(
    files=data,  # which files to consider
    add_general_data=True,  # whether should generate 'general' series
    group_by_minutes=5,  # group events by minutes; None disables it
    only_fatal=True,  # ignore non-fatal accidents
    date_conds=[
        {'day': 24, 'month': 12},
        {'day': 25, 'month': 12},
        {'day': 26, 'month': 12},
        # {'day': None, 'month': 2, }
    ],
    ignore_weekday=True
)
