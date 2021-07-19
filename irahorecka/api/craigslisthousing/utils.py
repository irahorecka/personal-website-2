"""
"""
import json
from pathlib import Path


NEIGHBORHOOD_PATH = Path(__file__).absolute().parent.joinpath("neighborhoods.json")


def open_json(input_path):
    """Opens JSON file from path and returns as dictionary."""
    with open(input_path) as file:
        data = json.load(file)
    return data


def write_json(data, output_path):
    """Takes dictionary data and output JSON path and writes dictionary to file.k"""
    with open(output_path, "w") as file:
        json.dump(data, file)
