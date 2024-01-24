from argparse import ArgumentParser
from pathlib import Path

import pandas as pd

def parse_args():

    parser = ArgumentParser(
        "Skyline2IsoCor: Convert Skyline output to IsoCor input"
    )

    parser.add_argument(
        "input", type=str,
        help='Path to Skyline output file'
    )
    parser.add_argument(
        'output', type=str,
        help='Path to output IsoCor input data'
    )

    return parser

def _get_isotopologue_number(row):

    original = row["isotopologue"]
    if original == "[M-H]":
        row["isotopologue"] = "0"
        return row
    row["isotopologue"] = original[2:].split("C")[0]
    return row

def process(args):

    try:
        input_path = Path(args.input)
        data = pd.read_csv(str(input_path), sep=",")
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
    isocor_data = isocor_data.apply(_get_isotopologue_number, axis=1)
    print(f"Final dataframe:\n{isocor_data}")
    isocor_data.to_csv(args.output, sep="\t", index=False)

parser = parse_args()
args = parser.parse_args()
process(args)
