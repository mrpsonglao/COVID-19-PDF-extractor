# imports for file management
import glob, os
import json


# imports for Word DOCX management
import docx
from docx.document import Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph

# Code Reference: https://github.com/python-openxml/python-docx/issues/40
def iter_block_items(parent):
    """
    Yield each paragraph and table child within *parent*, in document order.
    Each returned value is an instance of either Table or Paragraph. *parent*
    would most commonly be a reference to a main Document object, but
    also works for a _Cell object, which itself can contain paragraphs and tables.
    """
    if isinstance(parent, Document):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        raise ValueError("something's not right")
    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)


def convert_docx_to_json(word_file, input_folder, intermediary_folder):
    # extract filename
    filename = word_file.split('\\')[-1]

    # open Word Doc
    print(f">>> Processing {word_file}")
    document = docx.Document(docx = word_file)

    # initialize empty json per document
    doc_json = {}

    # extract list of paragraphs and tables, in order
    # Rationale: extract the paragraph right before each table to get their "header name"
    block_list = [block for block in iter_block_items(document)]

    # extract all tables only
    table_ix_list = []
    for ix, block in enumerate(block_list):
        if isinstance(block, docx.table.Table):
            table_ix_list.append(ix)

    # extract tables
    num_tables = len(table_ix_list)
    print(f"Found {num_tables} tables in the Word doc.")

    # go through each table in the file
    # TODO: Parallelize the code if there's time. Too many for-loops
    for table_ix in table_ix_list:
        # extract table based on index
        table = block_list[table_ix]
        
        # extract paragraph text right before each table
        # remove whitespaec
        table_name = block_list[table_ix - 1].text.strip()
        table_as_list = []

        # extract cell values of each table
        for row in table.rows:
            row_as_list = []
            for cell in row.cells:
                row_as_list.append(cell.text)
            table_as_list.append(row_as_list)

        # save to json
        doc_json[table_name] = table_as_list

    # save as json for intermediary processing
    output_filename = filename.replace(".docx", ".json")
    with open(os.path.join(intermediary_folder, output_filename), 'w') as json_file:
        json.dump(doc_json, json_file)