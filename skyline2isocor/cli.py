from argparse import ArgumentParser
from pathlib import Path

import pandas as pd

def parse_args():

    parser = ArgumentParser(
        "Skyline2IsoCor: Convert Skyline output to IsoCor input"
    )

    parser.add_argument(
        "-i","--input", type=str,
        help='Path to input file to convert'
    )
    parser.add_argument(
        '-o', '--output', type=str,
        help='Path to output IsoCor input data'
    )

    return parser

def _get_isotopologue_number(row):

    original = row["isotopologue"]
    if original == "[M-H]" or original == "[M+H]":
        row["isotopologue"] = "0"
        return row
    row["isotopologue"] = original[2:].split("C")[0]
    return row

def validate_file_extension(path):
    """
    Ensure file extension is of expected type
    :param path: input pathlib path object
    :return:
    """

    if not path.exists():
        raise ValueError("Input path is not valid")
    ext = path.suffix
    if ext not in [".dat", ".tsv", ".txt"]:
        raise ValueError(f"Error in file extension. File should be of tabular format or .dat. Detected format: {ext}")
    return ext

def process(args):

    try:
        input_path = Path(args.input)
        file_ext = validate_file_extension(input_path)
        if not file_ext:
            raise ValueError("Error in file extension. File should be of tabular format or .dat")
        data = pd.read_csv(str(input_path), sep="\t")
    except Exception:
        print(f"There was an error while reading the data. Data path: {args.input}")
        raise
    print(f"Skyline data:\n{data}")
    columns = ["File Name", "Molecule Name", "Product Adduct", "Product Mz", "Total Area"]
    missing_cols = [col for col in columns if col not in data.columns]
    if missing_cols:
        raise ValueError(f"There are missing columns in the input data. Missing columns: {missing_cols}")
    column_mapping = {
        "File Name": "sample",
        "Molecule Name": "metabolite",
        "Product Adduct": "isotopologue",
        "Total Area": "area"
    }
    isocor_data = data.rename(column_mapping, axis=1).drop("Product Mz", axis=1)
    isocor_data.insert(loc=2, column="derivative", value="")
    isocor_data = isocor_data.apply(func=_get_isotopologue_number, axis=1)
    isocor_data = isocor_data.fillna(0)
    print(f"Final dataframe:\n{isocor_data}")
    isocor_data.to_csv(args.output, sep="\t", index=False)

def start_cli():
    parser = parse_args()
    args = parser.parse_args()
    process(args)
