# imports for file management
import glob, os
import json

# imports for Word DOCX management
import docx

# import helper functions
from utils import convert_docx_to_json

# imports for data munging
import pandas as pd

# Setup file directories
input_folder = "raw_dromic"
intermediary_folder = "intermediary_output_json"
output_folder = "output_csv"

if not os.path.exists(intermediary_folder):
    os.makedirs(intermediary_folder)

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# get file list of word files
word_file_list = glob.glob(os.path.join(input_folder, "*"))

### PARSING DOCX to TABLES
for word_file in word_file_list:
    convert_docx_to_json(word_file, input_folder, intermediary_folder)