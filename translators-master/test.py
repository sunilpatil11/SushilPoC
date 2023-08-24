from googletrans import Translator
import pandas as pd
import translators as ts
import time

# Load the Excel file using pandas
file_path = r'c:\Project\【守谷LC】2023年7月_monthly Report (1).xlsx'
xls = pd.ExcelFile(file_path)

# Create a translator object
translator = Translator()

# Translate and save to a new Excel file
output_file_path = r'c:\Project\translated-monthly14.xlsx'
writer = pd.ExcelWriter(output_file_path, engine='xlsxwriter')

def clean_string(value):
    # Replace invalid characters with an underscore
    cleaned_value = value.replace(':', '_').replace('/', '_').replace('\\', '_').replace('?', '_').replace('*', '_').replace('[', '_').replace(']', '_')
    return cleaned_value

def truncate_sheet_name(sheet_name):
    # Truncate sheet name if it's too long
    max_length = 31  # Maximum allowed length for Excel sheet names
    if len(sheet_name) > max_length:
        truncated_name = sheet_name[:max_length]
        return truncated_name
    return sheet_name

def translate_sheet_name(sheet_name):
    try:
        translated_name = translator.translate(sheet_name).text
        cleaned_translated_name = clean_string(translated_name)
        truncated_translated_name = truncate_sheet_name(cleaned_translated_name)
        return truncated_translated_name
    except Exception as e:
        print("Sheet Name Translation Error:", e)
        return truncate_sheet_name(clean_string(sheet_name))

def translate_to_english():
    translator = Translator()
    for sheet_name in xls.sheet_names:
        translated_sheet_name = translate_sheet_name(sheet_name)
        df = pd.read_excel(xls, sheet_name)
        translated_data = []

        for index, row in df.iterrows():
            translated_row = []
            for cell in row:
                if isinstance(cell, str) and cell.strip():  # Check if the cell is a non-empty string
                    try:
                        translation = ts.translate_text(cell)
                        # translation = translator.translate(tran).text
                        translated_row.append(translation)
                    except Exception as e:
                        try:
                            translation = translator.translate(cell).text
                            translated_row.append(translation)
                        except:
                            pass
                        print("Translation Error:", e)
                        translated_row.append(cell) 
                    time.sleep(1)  # Wait for 1 second between requests
                else:
                    translated_row.append(cell)
            translated_data.append(translated_row)

        # if len(translated_df.columns) == len(df.columns):
        print("Row with mismatched columns in sheet:", translated_sheet_name)
        print("Original row:", row)
        print("Translated row:", translated_row)
        translated_df = pd.DataFrame(translated_data)
        translated_df.to_excel(writer, sheet_name=translated_sheet_name)


    writer._save()
    print("Translation complete. Translated data saved to", output_file_path)

