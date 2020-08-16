import convert, upload, helper_functions, sys

args = sys.argv
args.pop(0)
print(args)

# if program is run with no args, check if environment is correct
if len(args) == 1:
    helper_functions.create_environment()

# manually get new verification key
elif "-v" in args:
    helper_functions.get_access_token()
    
elif "-c" in args:
    # convert all files in INPUT folder
        convert.convert_all()
#     # convert specific file
#     else:
#         convert.convert_single()
        
elif "-u" in args:
    # upload all files in OUTPUT folder
        upload.add_all()
#     # upload specific file
#     else:
#         upload.add_single()
