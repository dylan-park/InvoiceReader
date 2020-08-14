from invoice2data import extract_data
from invoice2data.extract.loader import read_templates
from invoice2data.input import pdftotext as pdftotextdef
from invoice2data.output import to_json
from datetime import datetime
import helper_functions, os, pdftotext, json


# try to convert every file in the INPUT folder
def convert_all():
    # clear error file
    helper_functions.clear_errors()
    # loop through every pdf file in input folder
    for filename in os.listdir('INPUT/'):
        if filename.endswith(".pdf"): 
            read_file(filename, False)
            continue
        else:
            continue


# reads a pdf file and parses the data to JSON
def read_file(filename, debug):
    # If debug is active, get PDF as string for debugging/template creation
    if debug is True:
        with open('INPUT/' + filename, 'rb') as f:
            pdf = pdftotext.PDF(f)
        print('\n\n'.join(pdf))
        
    templates = read_templates('TEMPLATES/')
    result = extract_data('INPUT/' + filename, templates, pdftotextdef)
    # if pdf read successful write JSON file
    if result != False:
        to_json.write_to_file(result, 'OUTPUT/' + os.path.splitext(filename)[0] + '.json', '%Y-%m-%d')
        
        # checks if due_date present in JSON and if not sets due date 1 month after invoice date
        with open('OUTPUT/' + os.path.splitext(filename)[0] + '.json', 'r+') as file:
            data = json.load(file)
            if "date_due" not in data:
                date = data["date"]
                date_obj = datetime.strptime(date, '%Y-%m-%d')
                json_in = {"date_due":helper_functions.add_month(date_obj).strftime('%Y-%m-%d')}
                data.update(json_in)
                file.seek(0)
                json.dump(data, file, indent=4, sort_keys=True)
    # else add file name to error list and move on
    else:
        helper_functions.append_error(filename)
