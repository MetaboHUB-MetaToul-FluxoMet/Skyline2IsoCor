from argparse import ArgumentParser
from pathlib import Path
import re

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

# Singly charged ions, unlabelled ([M-H]) or with a number of 13C ([M3C13-1H])
ADDUCT_PATTERN = re.compile(r"\[M(?:(\d+)C13)?[+-]1?H\]")


def _get_isotopologue_number(adduct, molecule):
    """
    Get the isotopologue number from a Skyline product adduct
    :param adduct: Skyline product adduct, e.g. [M-H] or [M3C13-1H]
    :param molecule: molecule name, used in the error message
    :return: number of 13C in the isotopologue
    """

    match = ADDUCT_PATTERN.fullmatch(adduct)
    if match is None:
        raise ValueError(
            f"Unsupported Product Adduct '{adduct}' for molecule '{molecule}'. "
            f"Expected [M-H], [M+H] or a 13C-labelled form such as [M3C13-1H]"
        )
    return int(match.group(1) or 0)

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
    isocor_data["isotopologue"] = [
        _get_isotopologue_number(adduct, molecule)
        for adduct, molecule in zip(isocor_data["isotopologue"], isocor_data["metabolite"])
    ]
    isocor_data = isocor_data.fillna(0)
    print(f"Final dataframe:\n{isocor_data}")
    isocor_data.to_csv(args.output, sep="\t", index=False)

def start_cli():
    parser = parse_args()
    args = parser.parse_args()
    process(args)
