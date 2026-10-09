from pathlib import Path

import pandas as pd
import pytest

from skyline2isocor.cli import parse_args, process

TEST_DATA = Path(__file__).resolve().parents[1] / "skyline2isocor" / "test-data"


def convert(tmp_path, skyline_data):
    skyline_file = tmp_path / "skyline_output.tsv"
    output_file = tmp_path / "isocor_input.tsv"
    skyline_data.to_csv(skyline_file, sep="\t", index=False)
    process(parse_args().parse_args(["-i", str(skyline_file), "-o", str(output_file)]))
    return pd.read_csv(output_file, sep="\t")


def skyline_rows(*adducts):
    return pd.DataFrame({
        "File Name": "sample.raw",
        "Molecule Name": "Citrate",
        "Product Adduct": list(adducts),
        "Product Mz": 191.02,
        "Total Area": 1000.0,
    })


def test_test_data_conversion(tmp_path):
    result = convert(tmp_path, pd.read_csv(TEST_DATA / "skyline_output.csv"))
    expected = pd.read_csv(TEST_DATA / "output_test.tsv", sep="\t")
    pd.testing.assert_frame_equal(result, expected)


def test_isotopologue_numbers(tmp_path):
    result = convert(tmp_path, skyline_rows("[M-H]", "[M+H]", "[M3C13-1H]", "[M12C13+1H]"))
    assert list(result["isotopologue"]) == [0, 0, 3, 12]


@pytest.mark.parametrize("adduct", ["[M+Na]", "[M-2H]", "[M2N15-1H]"])
def test_unsupported_adducts_are_rejected(tmp_path, adduct):
    with pytest.raises(ValueError, match="Citrate"):
        convert(tmp_path, skyline_rows("[M-H]", adduct))
