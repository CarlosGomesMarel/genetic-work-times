import csv

def csv_to_dict(csv_file_path):
    csv_file = open(csv_file_path, 'rt')
    csv_file.seek(0)
    sniffdialect = csv.Sniffer().sniff(csv_file.read(10000), delimiters='\t,;')
    csv_file.seek(0)
    dict_reader = csv.DictReader(csv_file, dialect=sniffdialect)
    csv_file.seek(0)
    dict_data = []
    for record in dict_reader:
        dict_data.append(record)

    csv_file.close()

    return dict_data

def convert_input_data(csv_file_path):
    input_data = csv_to_dict(csv_file_path)

    raw = {}
    values = []

    for row in input_data:
        data = []
        for key in row.keys():
            data.append(int(row[key]))
        values.append(data)

    names = input_data[0].keys()
    for name in names:
        raw[name] = []
        
    for row in input_data:
        for key in row.keys():
            raw[key].append(int(row[key]))

    return raw, values

# csv_file_path = r'c:\\temp\\WorkTimes.csv'
# raw, values = convert_input_data(csv_file_path)
# print(raw)
