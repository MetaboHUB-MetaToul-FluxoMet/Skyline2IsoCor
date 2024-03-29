# Skyline2IsoCor

**Command-line tool to prepare skyline output data for use in IsoCor software.**

It is one of the routine tools used on the [MetaToul Platform](https://www6.toulouse.inrae.fr/metatoul)

The code is open-source, and available on [GitHub](https://github.com/MetaboHUB-MetaToul-FluxoMet/Skyline2IsoCor) under a GPLv3 license.

## Quick-start

Skyline2isocor requires Python 3.9 or higher and runs on all platforms.

Use `pip` to install Skyline2isocor from *pypi*:

```bash
$ pip install skyline2isocor
```

Run the command line interface:

```bash
$ skyline2isocor -i PATH_TO_DATA_FILE -o PATH_TO_OUTPUT_FILE
```

**PATH_TO_DATA_FILE** : path to your file with file name and extension (must be tsv or tab-separated txt file).

**PATH_TO_OUTPUT_FILE** : path to where the output file should be generated. The generated file name and extension (.tsv) must be given also.

