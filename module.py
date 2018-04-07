import pprint
import statistics


def cast(type_, value, default='null'):
    try:
        return type_(value)
    except ValueError:
        return default


def detect_type(column, null_values=('null', None), types=(float, str)):
    for cell in column:
        if cell in null_values:
            continue
        types_copy = list(types)
        for type_ in types:
            try:
                type_(cell)
            except ValueError:
                types_copy.remove(type_)
        types = types_copy
    return types[0]


def load_csv(filename):
    with open(filename) as f:
        rows = [row.split(',') for row in f.read().split('\n')][:-1]
        headers = rows.pop(0)
        return headers, rows, [[row[i] for row in rows] for i in range(len(headers))]


def get_column_stat(column: list, type_, null_values=('null', None)):
    rep = {
        'null_number': sum([column.count(null_value) for null_value in null_values])
    }
    error = 'error'
    column = [cast(type_, cell, error) for cell in column if cell not in null_values]
    rep['unreadable'] = column.count(error)
    column = [cell for cell in column if cell != error]
    if type_ is float:
        for cell in column:
            assert isinstance(cell, type_), cell
        rep['mean'] = statistics.mean(column)
        try:
            rep['harmonic_mean'] = statistics.harmonic_mean(column)
        except statistics.StatisticsError:
            rep['harmonic_mean'] = None
        rep['max'] = max(column)
        rep['min'] = min(column)
        rep['median'] = statistics.median(column)
        rep['std_dev'] = statistics.pstdev(column)
        try:
            rep['most_frequent'] = statistics.mode(column)
        except statistics.StatisticsError:
            rep['most_frequent'] = None
    elif type_ is str:
        for value in set(column):
            rep[value] = column.count(value)
    return rep


def main():
    headers, rows, columns = load_csv('data/boxes.csv')
    for header, col in zip(headers, columns):
        print(header)
        pprint.pprint(get_column_stat(col, detect_type(col)))


if __name__ == '__main__':
    main()
