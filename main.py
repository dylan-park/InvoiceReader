import invoice_reader, os
from invoice2data.extract.invoice_template import InvoiceTemplate

# # clear error file
# invoice_reader.clear_errors()
# # loop through every pdf file in input folder
# for filename in os.listdir('INPUT/'):
#     if filename.endswith(".pdf"): 
#         invoice_reader.read_file(filename, False)
#         continue
#     else:
#         continue

invoice_reader.add_expense(123, "2020-08-12", "Dylan Park")
# print(invoice_reader.upload_image())