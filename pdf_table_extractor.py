import tabula
import glob, os
import pandas as pd

def extract_table_data(input_filename, input_folder, output_folder, pages_to_extract="all"):
    # define unique_id_col = used to "group together" similar entities
    # define column boundaries
    if "SARO" in input_filename:
        unique_id_col = 'SARO NUMBER'
        columns = [127.602, 213.282,300.492,392.292,511.632,609.552,739.602,1027.242]
    elif "NCA" in input_filename:
        unique_id_col = 'NCA NUMBER'
        columns = [129.132,176.562,268.362,361.692,474.912,586.602,712.062,797.742, 1028.772,1146.582]

    ### DATA EXTRACTION
    # Read pdf as DataFrame
    df = tabula.read_pdf(input_filename, pages=pages_to_extract, stream=True, guess=False, columns=columns)
    print(f"Extracted {input_filename}")
    print(f"Detected columns: {df.columns}")

    ### DATA CLEANING
    print("Applying data cleaning protocols ...")
    # remove unnecessary blank columns
    df_clean = df.dropna(how='all', axis=1)

    # fill forward unique_id_col
    df_clean.loc[:, unique_id_col] = df_clean[unique_id_col].ffill(axis=0)

    # replace NaN with empty string for all other columns
    df_clean = df_clean.fillna("")

    # remove all repeating header columns
    df_clean = df_clean[df_clean[unique_id_col] != unique_id_col].reset_index(drop=True)
    id_list_original_order = df_clean[unique_id_col].unique()

    # set id col as index
    df_clean = df_clean.set_index(unique_id_col)

    # extract column names
    cols = df_clean.columns

    # merge all text data by id column
    all_clean_series = []
    for col in cols:
        df_temp = df_clean.groupby(unique_id_col)[col].apply(lambda x: ' '.join(list(x)).strip())
        all_clean_series.append(df_temp)

    # combine all merged columns, joined on id column
    df_final = pd.concat(all_clean_series, axis=1)

    # reindex the final output based on original list order
    df_final = df_final.reindex(id_list_original_order)

    ### DATA EXPORT
    # export the data as csv
    output_filename = input_filename.replace(".PDF", ".csv").replace(".pdf", ".csv").replace(input_folder, output_folder)
    df_final.to_csv(output_filename)
    print(f"Exported the data as: {output_filename}")


if __name__ == "__main__":
    input_folder = "raw"
    output_folder = "output_csv"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    input_filename_list = glob.glob(os.path.join(input_folder, "*"))

    for input_filename in input_filename_list:
        extract_table_data(input_filename, input_folder, output_folder, pages_to_extract="all")
