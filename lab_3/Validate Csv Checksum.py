import csv
import re
import os
import json
from checksum import calculate_checksum
import chardet

def detect_encoding(file_path):
    """
    Defines the encoding of the file.

    :param file_path: File path
    :return: String with encoding name
    """
    with open(file_path, 'rb') as file:
        raw_data = file.read(1000)
    result = chardet.detect(raw_data)
    return result['encoding']

def validate_csv(file_path, regex_patterns):
    """
    Checks the rows of the CSV file for matching regular expressions for each column.

    :param file_path: CSV file path
    :param regexp_pattern: List of regular expressions for checking columns
    :return: List of row numbers with errors
    """
    invalid_rows = []

    encoding = detect_encoding(file_path)
    with open(file_path, 'r', encoding=encoding) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        for row_number, row in enumerate(reader):
            for col_number, (value, pattern) in enumerate(zip(row, regex_patterns)):
                if not re.fullmatch(pattern, value):
                    invalid_rows.append(row_number)
                    break

    return invalid_rows

def serialize_result(file_path, variant, checksum):
    """
    Fills in result.json data: option number and checksum.

    :param file_path: Path to the result file.json
    :param variant: Variant number
    :param checksum: Checksum
    """
    with open(file_path, 'w', encoding='utf-8') as result_file:
        json.dump({"variant": variant, "checksum": checksum}, result_file, indent=4)

def load_paths(config_path):
    """
    Loads paths from a JSON file.

    :param config_path: Path to the configuration file
    :return: Dictionary with paths
    """
    with open(config_path, 'r', encoding='utf-8') as config_file:
        return json.load(config_file)

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'config.json')

    paths = load_paths(config_path)


    column_patterns = [
        r"^\d{10}$",                        # telephone: 10 numbers
        r"^[A-Za-z ]+$",                    # http_status_message: text message
        r"^\d{10,12}$",                     # inn: 10-12 numbers
        r"^[A-Z]{2}-\d{6}$",                # identifier: two letters, a hyphen, 6 numbers
        r"^(?:\d{1,3}\.){3}\d{1,3}$",       # ip_v4: format xxx.xxx.xxx.xxx
        r"^-?\d{1,2}\.\d+$",                # latitude: fractional number from -90 to 90 
        r"^(A|B|AB|O)[+-]$",                # blood_type: blood groups (A+, O-, AB-, etc.)
        r"^\d{3}-\d{1,5}-\d{1,7}-\d{1,7}-\d{1}$",  # isbn: format ISBN
        r"^[a-f0-9]{8}-([a-f0-9]{4}-){3}[a-f0-9]{12}$",  # uuid: format UUID
        r"^\d{4}-\d{2}-\d{2}$"              # date: format YYYY-MM-DD
    ]

    csv_file_path = paths['csv_file_path']

    invalid_row_numbers = validate_csv(csv_file_path, column_patterns)

    checksum = calculate_checksum(invalid_row_numbers)

    result_file_path = paths['result_file_path']
    variant_number = 30
    serialize_result(result_file_path, variant_number, checksum)

    print(f"The checksum: {checksum}")
