import helper_functions, requests, json, os


# add all expenses from OUTPUT folder
def add_all():
    # loop through every pdf file in input folder
    for filename in os.listdir('OUTPUT/'):
        if filename.endswith(".json"):
            with open('OUTPUT/' + filename, 'r') as f:
                json_object = json.loads(f.read())
            amount = json_object["amount"]
            date = json_object["date_due"]
            vendor = json_object["issuer"]
            name = filename.split(".")[0]
            add_expense(name, amount, date, vendor)
            continue
        else:
            continue

# def add_single(filepath):


# add new expense to FreshBooks account
def add_expense(filename, amount, date, vendor):
    access_token = helper_functions.check_access_token()
    # url for post request  
    image_object = helper_functions.upload_image(filename)
    with open('credentials.json', 'r') as f:
        credentials_json = json.loads(f.read())
    x = requests.post('https://api.freshbooks.com/accounting/account/' + credentials_json['account_id'] + '/expenses/expenses',
                      # JSON data to send
                      json={"expense": 
                            {"amount": { "amount": amount},
                             "categoryid": credentials_json['categoryid'],
                             "staffid": credentials_json['staffid'],
                             "date": date,
                             "vendor": vendor,
                             "attachment":
                            {"jwt": image_object["jwt"],
                             "media_type": image_object["media_type"]
                                }}},
                      # header to send with request
                      headers={"Api-Version": "alpha",
                               "Content-Type": "application/json",
                               "Authorization": "Bearer " + access_token})
    if (x.status_code == 200):
        print(filename + " Uploaded")
