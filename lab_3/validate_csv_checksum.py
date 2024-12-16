import csv
import re
import os
import json
from checksum import calculate_checksum


def is_invalid(regex_patterns: dict, data: list) -> bool:
    """
        Searches for invalid lines in a csv file
    Args:
        regex_patterns (dict): patterns for text processing
        data (list): a string from a csv file

    Returns:
        bool: invalid or valid
    """
    return not all(re.match(regex_patterns[key], value) for key, value in zip(regex_patterns, data))

def validate_csv(data: list, regex_patterns: dict) -> list[int]:
    """
        Returns indexes of all invalid rows

    Args:
        patregex_patternstern (dict):  patterns for text processing
        data (list): csv file

    Returns:
        list[int]: indexes of all invalid rows
    """
    return [index for index, value in enumerate(data) if is_invalid(regex_patterns, value)]

def serialize_result(file_path: str, variant: int, checksum: str) -> None:
    """
    Fills in result.json

    :param file_path: Path to the result file.json
    :param variant: Variant number
    :param checksum: Checksum
    """
    with open(file_path, 'w', encoding='utf-8') as result_file:
        json.dump({"variant": variant, "checksum": checksum}, result_file, indent=4)

def read_csv(path: str) -> list[list[str]]:
    """
        Reads the csv file and takes the necessary lines
    Args:
        path (str): the path to the file

    Returns:
        list: csv file lines except column names
    """
    try:
        with open(path, "r", encoding="utf-16") as file:
            info_file = csv.reader(file, delimiter=";")
            first_line = next(info_file, None)
            return [line for line in info_file] if first_line else []
    except Exception as e:
        print(f"Exception in read_csv: {e}")

def read_json(path: str) -> dict[str, str]:
    """
    Loads paths from a JSON file.

    :param config_path: Path to the configuration file
    :return: Dictionary with paths
    """
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'config.json')

    paths = read_json(config_path)

    regex_patterns = read_json(paths['regex_patterns'])
    data = read_csv(paths['csv_file_path'])

    invalid_row_numbers = validate_csv(data, regex_patterns)
    print(invalid_row_numbers)

    checksum = calculate_checksum(invalid_row_numbers)

    result_file_path = paths['result_file_path']
    variant_number = 30
    serialize_result(result_file_path, variant_number, checksum)

    print(f"The checksum: {checksum}")
