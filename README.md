# COVID-19 PDF extractor
Version: 0.1

As of: Apr. 4, 2020

License: MIT

## Overview
Rough Python script which uses `tabula-py` to extract data from DBM PDF files and outputs these as CSV.

For more on `tabula-py`, see [here](https://tabula-py.readthedocs.io/en/latest/).

### Inputs: 
DBM PDF files in the `raw` folder, which should be either:
- Special Allotment Release Order (SARO) data
- or Notice of Cash Allocation (NCA) data

> Note: There are already 2 sample inputs currently in the `raw` folder, in particular:
> - `UPDATED_SARO.pdf`: [Original SARO data as PDF updated as of 3 April 2020 (274 pages)](https://www.dbm.gov.ph/index.php/programs-projects/special-allotment-release-order-saro)
> - `UPDATED_NCA.pdf`: [Original NCA data as PDF updated as of 3 April 2020 (800 pages)](https://www.dbm.gov.ph/index.php/programs-projects/notice-of-cash-allocation-nca-listing)

### Outputs:
CSV files in `output_csv` folder.

> Note: There are already 2 sample outputs currently in the `output_csv` folder, in particular:
> - `UPDATED_SARO.csv`: Extracted SARO data extracted as of 4 April 2020 (5,113 unique transaction rows)
> - `UPDATED_NCA.csv`: Extracted NCA data extracted as of 4 April 2020 (12,305 unique transaction rows)

## Scope & Limitations
- The script has data extraction and cleaning protocols specific to SARO and NCA PDF data structures. It cannot extract data for other kinds of PDF files which have a different structure.
- The input PDF data is assumed to either have the partial text `"SARO"` or `"NCA"` in their filenames, since a partial string match is used to identify the data cleaning process to apply to the PDF. 
- Assumed unique transaction identifiers:
    - For SARO data: `SARO NUMBER`
    - For NCA data: a combination of `NCA NUMBER`, `NCA TYPE`, and implicit "row index"
- Forward-filling of data was done for NCA, with the assumption that cells which are blank but pertaining to the same `NCA NUMBER` are implied to have the same data for these columns: 
    ```
    ['APPROVED DATE', 'RELEASED DATE', 'DEPARTMENT', 'AGENCY', 'PURPOSE']
    ```

## Prerequisites & Setup
Caveats:
- The code uses Python 3.7.6.
- This has only been tested on a Windows 10 64-bit machine.

### Environment setup
To replicate this on your own machines:

1. Clone this Github repository.
2. Go to the repository's root directory. Then, install all Python package dependencies via command prompt:

    ```
    pip install -r requirements.txt
    ```

## Running the code
1. Setup the environment as seen above in [**Environment setup**](#environment-setup).
2. Add your new SARO or NCA PDF files in the `raw` folder.
    - **IMPORTANT NOTE:** The input PDF data is assumed to either have the partial text `"SARO"` or `"NCA"` in their filenames, since a partial string match is used to identify the data cleaning process to apply to the PDF. Make sure the filename contains one of these key substrings!
    - Feel free to delete existing PDF files in the `raw` folder.
    - Note that the script will convert **all** PDF files in the `raw` folder, so only add valid SARO or NCA PDF files there.

3. Go to the repository's root directory. Then, run:

    ```
    python pdf_table_extractor.py
    ```
    
    You should see some printed statements on your console to give a sense of what the program is doing.
    
4. This will generate the extracted data as CSV in the `output_csv` directory.

    Note that the filename of the extracted CSVs will be the same as that of your input PDF files, only that the file extension will be changed from `.pdf` to `.csv`.

## Feedback and suggestions
For feedback and suggestions, please email me at mrpsonglao@gmail.com. Feel free to send a pull request if you want to contribute as well.
