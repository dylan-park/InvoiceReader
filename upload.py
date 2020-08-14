import helper_functions, requests, json


# add new expense to Catalyst Content FreshBooks account
def add_expense(amount, date, vendor):
    access_token = helper_functions.check_access_token()
    # url for post request  
    image_object = helper_functions.upload_image()
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
    # print the returned data from the post request for verification
    print(x.text)
