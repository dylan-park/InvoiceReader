import invoice_reader, os

# clear error file
invoice_reader.clear_errors()
# loop through every pdf file in input folder
for filename in os.listdir('INPUT/'):
    if filename.endswith(".pdf"): 
        invoice_reader.read_file(filename, False)
        continue
    else:
        continue
