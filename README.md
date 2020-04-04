# COVID-19 PDF extractor
Version: 0.1
As of: Apr. 4, 2020

## Overview
Rough Python script which uses `tabula-py` to extract data from DBM PDF files and outputs these as CSV.

### Inputs: 
DBM PDF files, in particular:

- Special Allotment Release Order (SARO) data in PDF (274 pages, last updated 3 April 2020): https://www.dbm.gov.ph/index.php/programs-projects/special-allotment-release-order-saro
- Notice of Cash Allocation (NCA) data in PDF (800 pages, last updated 3 April 2020):
https://www.dbm.gov.ph/index.php/programs-projects/notice-of-cash-allocation-nca-listing

### Outputs:
CSV files in `output_csv` folder

## Scope & Limitations
- The script has data extraction and cleaning protocols specific to SARO and NCA PDF data structures. It cannot extract data for other kinds of PDF files which have a different structuer.
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
1. Setup the environment as seen above in **Environment setup**.
2. Add your new SARO or NCA PDF files in the `raw` folder. 
3. Go to the repository's root directory. Then, run:
```
python pdf_table_extractor.py
```
4. This will generate the extracted data as CSV in the `output_csv` directory.
    - Note that the filename of the extracted CSVs will be the same as that of your input PDF files, only that the file extension will be changed from `.pdf` to `.csv`.

## Feedback and suggestions
For feedback and suggestions, please email me at mrpsonglao@gmail.com. Feel free to send a pull request if you want to contribute as well.